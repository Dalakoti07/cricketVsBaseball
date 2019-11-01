from tensorflow.keras.applications import MobileNetV2
# this line in cmd is asking for path itself
from flask import Flask, session,redirect,url_for,render_template,request,jsonify
import requests
base_model =MobileNetV2(input_shape=(160,160,3),include_top=False,weights='imagenet')

from tensorflow.keras.layers import Dense,GlobalAveragePooling2D
from tensorflow.keras.layers import Dropout
x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dropout(0.2)(x)
x=Dense(512,activation='relu')(x) #dense layer 2
x=Dropout(0.2)(x)
x=Dense(256,activation='relu')(x) #dense layer 3
preds=Dense(2,activation='softmax')(x) #final layer with softmax activation

from tensorflow.keras.models import Model
model=Model(inputs=base_model.input,outputs=preds)

model.load_weights('SixthTraining.h5')

from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
import numpy as np
import argparse
import random
import cv2
import os


def weAreLive(url):
    pic_url=url
    with open('test.jpg', 'wb') as handle:
            response = requests.get(pic_url, stream=True)

            if not response.ok:
                print (response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
#     preprocessing the image 
    image = cv2.imread('test.jpg')
    image = cv2.resize(image, (160,160))
    image = img_to_array(image)

#         Making the predictions
    res=model.predict(np.expand_dims(testX[indx], axis=0))
    if res[0][0]>res[0][1]:
        return "Baseball"
    else:
        return "Cricket"
#     deleting the file at last
    os.remove("test.jpg")
    



@app.route("/")
def index():
    return render_template('home.html')

# request would be made from js code
@app.route("/predict",methods=["POST"])
def fetchdata():
    # what if user didnot apply any filter
    x=request.form.get("url")
    res=weAreLive(x)
    return json.dumps({"res":res})

# if __name__ == '__main__':
# 	app.debug=True
# 	app.run()
