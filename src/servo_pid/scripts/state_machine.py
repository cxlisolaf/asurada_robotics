#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64

ce_straight = 0
ce_corner = 0
# State input from IR sensor, data in is average distance from center of hallway
# Negative value = Left of Center
# Positive value = Right of Center


def callback(data):

    if data.data < -180 and dist_left < 400:
        control_pub.publish(ce_straight)
        rospy.loginfo('CORNER!')
    else:
        control_pub.publish(ce_straight)
        rospy.loginfo('FULL SPEED AHEAD!')

#    print data.data
#    if data.data < -250:
#        control_pub.publish(ce_corner)
#        rospy.loginfo('CORNER!')
#    else:
#        control_pub.publish(ce_straight)
#        rospy.loginfo('FULL SPEED AHEAD!')

def cb_straight(data):
#    print data.data
    global ce_straight
    ce_straight = data.data

def cb_corner(data):
#    print data.data
    global ce_corner
    ce_corner = data.data

def cb_right(right):
    global dist_right
    dist_right = right.data

def cb_left(left):
    global dist_left
    dist_left = left.data

def main():
    #initialize state_machine node
    rospy.init_node('state_machine', anonymous=True)
    # create publisher object and map to "control_pub" variable. Publish to "/control_input"
    # topic which the pololupub.py subscribes to.
    global control_pub
    control_pub = rospy.Publisher('control_input', Float64, queue_size=10)
    # rate = rospy.Rate(100)
    rospy.Subscriber('ce_straight', Float64, cb_straight)
    rospy.Subscriber('ce_corner', Float64, cb_corner)
    rospy.SubcriberI('dist_right', Float64, cb_right)
    rospy.Subcriber('dist_left', Float64, cb_left)
    rospy.Subscriber('state', Float64, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
