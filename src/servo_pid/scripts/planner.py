#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64


# setpoint publisher plublish to "setpoint" topic
setpoint_pub = rospy.Publisher('setpoint', Float64, queue_size=10)
rospy.init_node('setpoint_pub', anonymous=True)

setpoint = Float64()
setpoint.data = float(0)

class Straight(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
        rospy.loginfo('Straight')

class Corner(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
        rospy.loginfo('Corner')
        re


def set_message():
    while not rospy.is_shutdown():
        setpoint_pub.publish(setpoint)
        rospy.sleep(.02) #50 hz


if __name__ == '__main__':
    try:
        set_message()
    except rospy.ROSInterruptException:
        pass
