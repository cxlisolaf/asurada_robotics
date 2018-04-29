#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import maestro

def listener():

    rospy.init_node("control_stop",anonymous = True)
    rospy.Subscriber("seestop",Image,callback, queue_size=1)
    rospy.spin()

def callback(data):
    try:
	if data == True:
	   maestro.Controller().setTarget(1,2000)
	else:
	   maestro.Controller().setTarget(1,6000)
		
    except CvBridgeError as e:
        print e


if __name__ == '__main__':

    try:       
       listener()

    except rospy.ROSInterruptException:
        pass

