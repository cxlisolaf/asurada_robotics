#!/usr/bin/env python

#import maestro
import rospy
from std_msgs.msg import Float64
from opencv_apps.msg import FlowArrayStamped


def callback(flows):
    rospy.loginfo(flows.data)

def subscriber():
    rospy.Subcriber('flows', FlowArrayStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass
