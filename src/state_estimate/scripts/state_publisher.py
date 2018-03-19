#!/usr/bin/env python
import maestro
import rospy
from std_msgs.msg import Float64
from transform import transform

CHANNEL_L_IR = 6
CHANNEL_R_IR = 11
WINDOW_SIZE = 50

def publisher():
    pub = rospy.Publisher('state', Float64, queue_size=10)
    rospy.init_node('state_estimate', anonymous=True)
    rate = rospy.Rate(50)
    pololu = maestro.Controller()
    window = [0] * WINDOW_SIZE
    index = 0
    while not rospy.is_shutdown():
        ir_left = pololu.getPosition(CHANNEL_L_IR)
        dist_left = transform(ir_left)
        print 'ir left: ' + str(ir_left)
        print 'dist left: ' + str(dist_left)
        ir_right = pololu.getPosition(CHANNEL_R_IR)
        dist_right = transform(ir_right)
        print 'ir right: ' + str(ir_right)
        print 'dist right: ' + str(dist_right)
        diff = dist_left - dist_right
        window[index] = diff
        index += 1
        index %= WINDOW_SIZE
        average = sum(window) / WINDOW_SIZE
        pub.publish(average)
        print 'ir diff: ' + str(ir_left - ir_right)
        print 'dist diff: ' + str(diff)
        print 'average: ' + str(average)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
