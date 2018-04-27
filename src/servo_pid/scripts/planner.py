#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64

#global rate
#rate = rospy.Rate(50) #in Hz


# setpoint publisher object plublish to "/setpoint" topic
setpoint_pub = rospy.Publisher('/setpoint', Float64, queue_size=10)
rospy.init_node('setpoint_pub', anonymous=True)

#Setpoint message in Float64 format
setpoint = Float64()
setpoint.data = float(0)

def set_message():
    while not rospy.is_shutdown():
        setpoint_pub.publish(setpoint)
        rospy.sleep(0.02)


if __name__ == '__main__':
    try:
        set_message()
    except rospy.ROSInterruptException:
        pass
