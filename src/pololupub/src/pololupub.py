#!/usr/bin/env python

import maestro
import rospy
from std_msgs.msg import Float64


def callback():
    rospy.loginfo("I heard PID")
    pwn = data.data
    pololu = maestro.Controller()
    pololu.setTarget(0, 6000-pwn)

def subscriber():
    rospy.init_node('pololu_sub', anonymous=True)

    rospy.Subscriber("Control_Effort", Float64, callback)
                                                                         
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
                                                                                             

if __name__ == '__main__':
    try:
        pololu = maestro.Controller()
        pololu.setSpeed(1, 2000)
        pololu.setTarget(1, 6600)
        print 'motor'
        subscriber()

    except rospy.ROSInterruptExecution:
        pass
