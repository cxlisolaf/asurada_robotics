#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import maestro
from std_msgs.msg import Bool
def listener():

    rospy.init_node("control_stop",anonymous = True)
    rospy.Subscriber("/seestop",Bool,callback)
    print("I listen")
    rospy.spin()

def callback(data):
    try:
        print(data.data)
	if data.data == True:
	   print data.data
	   maestro.Controller().setTarget(1,6300)
	else:
	   maestro.Controller().setTarget(1,2000)
		
    except CvBridgeError as e:
        print e


if __name__ == '__main__':

    try:       
       listener()

    except rospy.ROSInterruptException:
        pass

