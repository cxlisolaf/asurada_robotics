#!/usr/bin/env python

from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
from cv_bridge import CvBridge, CvBridgeError

model = load_model("stop_sign2.model)

def listener():

    rospy.init_node('image_classify',anonymous = True)
   
    rospy.Subscriber("/camera/image_raw", Image, callback)
    
    rospy.spin()


def callback(data):

    try:
        global counter
        counter += 1
        print("I heard")
        
        cv_image = CvBridge().imgmsg_to_cv2(data, "bgr8")
	cv2.imwrite("frame.jpg",cv_image)

        if counter%5 == 0:

	image = cv2.imread("frame.jpg")

	# pre-process the image for classification
	image = cv2.resize(image, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# load the trained convolutional neural network
	print "[INFO] loading network..."

	# classify the input image
	(nonstop, stop) = model.predict(image)[0]

	# build the label
	label = "stop" if stop > nonstop else "nonstop"
	proba = stop if stop > nonstop else nonstop
	label = "{}: {:.2f}%".format(label, proba * 100)

	print label

        if label == "stop":
            maestro.Controller().setTarget(1,3000)
        else:
            maestro.Controller().setTarget(1,6500)


    except CvBridgeError as e:
        
        print e


    cv2.waitKey(3)


if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Shutting down")



    cv2.destroyAllWindows()


