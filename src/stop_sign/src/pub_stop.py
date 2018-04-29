#!/usr/bin/env python

#import roslib

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import Bool

from cv_bridge import CvBridge, CvBridgeError
import os
import numpy as np

img_width, img_height = 150, 150
    
input_shape = (3, img_width, img_height)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))


model.load_weights('first_try.h5')


def detect(image):
   	
    img = load_img(image,False,target_size=(img_width,img_height))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict_classes(x)
    prob = model.predict_proba(x)
    print(preds, prob)

    return pred,prob

def listener():

    rospy.init_node('image_classify',anonymous = True)
    rospy.init_node('control', anonymous=True)

    rospy.Subscriber("/camera/image_raw", Image, callback)
    rospy.spin()


def callback(data):

    try:
        
        print("I heard")
        cv_image = CvBridge().imgmsg_to_cv2(data, "bgr8")
	pred, prob = detect(cv_image)
         
	rate = rospy.Rate(10) # 10hz
	pub = rospy.Publisher('seestop', Bool, queue_size=10)
        pub.publish(pred)

	rate.sleep()


	#cv2.imwrite("frame.jpg", cv_image) 



    except CvBridgeError as e:
        
        print(e)


    cv2.waitKey(3)


if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Shutting down")



    cv2.destroyAllWindows()


