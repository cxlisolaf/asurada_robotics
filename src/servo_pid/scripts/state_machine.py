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

index = 0
turn_counter = 0

def callback(data):
    global index
    global count 
    global turn_counter
    count = 10

    if turn_counter < 200: 
        control_pub.publish(int(0))
        turn_counter += 1
        rospy.loginfo(str(turn_counter))
        index = 0
    elif data.data < -180:
        control_pub.publish(ce_straight)
        if index == count:
            rospy.loginfo('CORNER!')
            index =0
    else:
        control_pub.publish(ce_straight)
        if index == count:
            rospy.loginfo('FULL SPEED AHEAD!')
            index = 0

    index += 1
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
    rospy.Subscriber('state', Float64, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
                pass
