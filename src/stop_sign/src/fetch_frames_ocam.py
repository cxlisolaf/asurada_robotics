import roslib

#roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
import numpy as np


i_image = 0



def listener():

    rospy.init_node('image_converter',anonymous = True)
    #rate = rospy.Rate(0.1)
    
    rospy.Subscriber("/camera/image_raw", Image, callback)
    rospy.sleep(10)

    rospy.spin()
    


def callback(data):

    try:
        
        cv_image = CvBridge().imgmsg_to_cv2(data,'bgr8')
	
        if i_image%100 == 0:
            img_name = "frame"+str(i_image)+".jpg"
	    cv2.imwrite(img_name, cv_image) 
            #img = cv2.imread("frame.jpg",0)
            print(i_image)

            #print("i detect")

        global i_image
        i_image += 1
	

    except CvBridgeError as e:
        print(e)


    cv2.waitKey(3)


if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()



