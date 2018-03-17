#!/usr/bin/env python

import maestro
import rospy
from std_msgs.msg import Float64


def callback():
    rospy.loginfo("I heard PID")
    pwn = data.data
    publisher(pid)


def publisher(pid):
    pub = rospy.Publisher('pololu', Float64, queue_size=10)
    rospy.init_node('pololu_pub', anonymous=True)
    rate = rospy.Rate(50)
    pololu = maestro.Controller()
    while not rospy.is_shutdown():
        pub.publish(pwn)
        rate.sleep()

                  
def subscriber():
    rospy.init_node('pololu_sub', anonymous=True)

    rospy.Subscriber("Control_Effort", Float64, callback)
                                                                         
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
                                                                                             

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptExecution:
        pass
