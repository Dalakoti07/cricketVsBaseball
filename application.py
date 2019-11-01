from flask import Flask, session,redirect,url_for,render_template,request,jsonify
import requests
from tensorflow.keras.models import model_from_json

json_file = open('model.json','r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#load woeights into new model
loaded_model.load_weights("ReTraining.h5")
print("Loaded Model from disk")

app = Flask(__name__)

# from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
import numpy as np
import argparse
import random
import cv2
import os
import requests

def weAreLive():
    pic_url=input('enter the url ')
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
#     cv2.imshow('ImageWindow',image)
#     cv2.waitKey()
#         Making the predictions
    res=loaded_model.predict(np.expand_dims(image, axis=0))
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
@app.route("/predict",methods=["POST","GET"])
def fetchdata():
    # what if user didnot apply any filter
    x=request.form.get("url")
    res=weAreLive(x)
    return json.dumps({"res":res})

if __name__ == '__main__':
	app.debug=True
	app.run()
