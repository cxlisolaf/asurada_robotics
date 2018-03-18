#!/usr/bin/env python
import maestro
import rospy
from std_msgs.msg import Float64

CHANNEL_L_IR = 6
CHANNEL_R_IR = 11

def publisher():
    pub = rospy.Publisher('state', Float64, queue_size=10)
    rospy.init_node('state_estimate', anonymous=True)
    rate = rospy.Rate(50)
    pololu = maestro.Controller()
    while not rospy.is_shutdown():
        left_dist = pololu.getPosition(CHANNEL_L_IR)
        print 'left: ' + str(left_dist)
        right_dist = pololu.getPosition(CHANNEL_R_IR)
        print 'right: ' + str(right_dist)
        diff = left_dist - right_dist
        pub.publish(diff)
        print diff
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
