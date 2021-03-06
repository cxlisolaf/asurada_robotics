#!/usr/bin/env python

import maestro
import rospy
from std_msgs.msg import Float64

#previously with old servo servo_center = 6300
#new servo servo_center =6000
SERVO_CENTER = 6100
#note to ryan 6450
motor_speed = 6470
pololu = maestro.Controller()



def callback(data):
#    rospy.loginfo("I heard PID: " + str(data.data))
    pwm = int(data.data)
    global pololu
# pololu.setAccel(0, 10)
    pololu.setTarget(0, SERVO_CENTER + pwm)
    pololu.setTarget(1, motor_speed)

def subscriber():
    rospy.init_node('pololu_sub', anonymous=True)

    rospy.Subscriber("control_input", Float64, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        # pololu = maestro.Controller()
        # pololu.setSpeed(1, 2000)
        # pololu.setTarget(1, 5000)
        subscriber()

    except rospy.ROSInterruptException:     
        pololu.setTarget(1, 6200)
        pass
