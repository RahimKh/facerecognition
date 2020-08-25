import cv2
import os
import numpy as np

from keras.models import model_from_json
import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior() 

UPLOAD_FOLDER = "/home/rahim/app/static"
MODEL_PATH = "model.json"
MODEL_WEIGHTS = "model.h5"



def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    pos_dist = tf.reduce_sum(tf.square(anchor-positive),axis=-1)
    neg_dist = tf.reduce_sum((anchor-negative)**2,axis=-1)
    basic_loss = tf.add(tf.subtract(pos_dist,neg_dist),alpha)
    loss = tf.reduce_sum(tf.maximum(basic_loss,0))    
    return loss


def verify(new_encoding, identity, encoded, model):
    dist = np.linalg.norm(new_encoding-encoded)
    if dist<0.7:
        continue_scan = True
    else:
        continue_scan = False
        
    return continue_scan


