import cv2
import os
import numpy as np
from mtcnn.mtcnn import MTCNN
from keras_vggface import VGGFace
from scipy.spatial.distance import cosine
from keras import backend as K
import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior() 
#K.set_image_data_format('channels_first')

UPLOAD_FOLDER = "/home/rahim/app/static"
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

class FRmodel:
    def __init__(self):
        self.model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
        self.model._make_predict_function()
        self.session=tf.keras.backend.get_session()
        self.graph=tf.get_default_graph()
    
    def predict_on_batch(self,img):
        with self.graph.as_default():
            with self.session.as_default():
                pred=self.model.predict_on_batch(img)
        return(pred)

'''def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    pos_dist = tf.reduce_sum(tf.square(anchor-positive),axis=-1)
    neg_dist = tf.reduce_sum((anchor-negative)**2,axis=-1)
    basic_loss = tf.add(tf.subtract(pos_dist,neg_dist),alpha)
    loss = tf.reduce_sum(tf.maximum(basic_loss,0))    
    return loss'''


def verify(new_encoding, encoded, model,thresh=0.5):
        score = cosine(encoded, new_encoding)
        if(score<0.5):
            continue_scan=True
            print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
        else:
            continue_scan=False
            print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
        return continue_scan

class FDmodel:
    def __init__(self):
        self.model=MTCNN()
        self.session=tf.keras.backend.get_session()
        self.graph=tf.get_default_graph()
    
    def detect_faces(self,img):
        with self.graph.as_default():
            with self.session.as_default():
                boxes=self.model.detect_faces(img)
        return boxes

