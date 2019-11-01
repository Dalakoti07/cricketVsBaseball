var urlObj = document.getElementById("url-id");
var predBtn = document.getElementById("predBtn");
predBtn.addEventListener("click", function() {
  let img = document.getElementById("img-id");
  img.scr = urlObj.value;
  img.style.visibility = "visible";
  console.log(urlObj.value);
});

// alert("hmm");
