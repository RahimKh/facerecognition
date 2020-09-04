import model 
import numpy as np 
import cv2
import os
import base64
import mysql.connector
import imageprocessing
import database


from PIL import Image
from io import BytesIO
from matplotlib import pyplot
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from mtcnn.mtcnn import MTCNN


#sess = tf.Session()
#graph = tf.get_default_graph()


app = Flask(__name__)
MODEL = None
MODEL_PATH = "model.json"
MODEL_WEIGHT = "model.h5"
UPLOAD_FOLDER = "./static/images/"
#TABLE = "image_vectorielle"
TABLE="encoding1"
#facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#set_session(sess)

detector = MTCNN()



@app.route("/api/facerec/reg",methods=["POST"])
def upload_predict():
    if request.method == "POST":
        #global graph
        #global sess
    
        #with graph.as_default():
        #    set_session(sess)
        payload = request.get_json()
        if (payload==None):
            payload=request.form.to_dict()
        if (payload==None):
            return jsonify({"msg":"fail,check payload"})
        print(payload['id'])
        print(len(payload["image"]))
        im_b64 = payload["image"]
        id = str(payload['id'])
        image_location=imageprocessing.image_decode(id,im_b64)
        imageprocessing.check_rotation(image_location)
        img=pyplot.imread(image_location)

        faces=detector.detect_faces(img)
        if (len(faces)==0):
            imageprocessing.change_dpi(image_location)
            img=pyplot.imread(image_location)
            faces=detector.detect_faces(img)
        if (len(faces)==0):
            os.remove(image_location)
            return jsonify({"msg":"Couldn't find face"})
        print(faces)
        img_encoded=imageprocessing.img_to_encoding(img,faces,MODEL)
        database.insert_to_base(id,img_encoded,TABLE)
        os.remove(image_location)
        return jsonify({"msg":"success",'id':id})

@app.route("/api/facerec/check",methods=["POST"])
def check():
    if request.method == "POST":
        #global graph
        #global sess
        #with graph.as_default():
        #    set_session(sess)
        payload = request.get_json()
        if (payload==None):
            payload=request.form.to_dict()
        if (payload==None):
            return jsonify({"msg":"fail,check payload"})
        im_b64 = payload["image"]
        id = str(payload['id'])
        image_location=imageprocessing.image_decode(id,im_b64)
        imageprocessing.check_rotation(image_location)
        img=pyplot.imread(image_location)
        faces=detector.detect_faces(img)
        if (len(faces)==0):
            imageprocessing.change_dpi(image_location)
            img=pyplot.imread(image_location)
            faces=detector.detect_faces(img)
        if (len(faces)==0):
            os.remove(image_location)
            return jsonify({"msg":"Couldn't find face"})
        new_encoding=imageprocessing.img_to_encoding(img,faces,MODEL)
        encoded=database.get_encoded_img(id,TABLE)
        checked=model.verify(new_encoding,id,encoded,MODEL)
        os.remove(image_location)
        return jsonify({'msg':'success' ,'PASS':checked})    

if __name__ == "__main__":
    
    MODEL=model.FRmodel(MODEL_PATH,MODEL_WEIGHT)
    from waitress import serve
    #serve(app,host="0.0.0.0",port="8080",threads=1)
    app.run(host='127.0.0.1', debug=False,threaded=False)