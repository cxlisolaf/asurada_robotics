#!/usr/bin/env python
import maestro
import rospy
from std_msgs.msg import Float64
from transform import transform

CHANNEL_L_IR = 6
CHANNEL_R_IR = 11
WINDOW_SIZE = 10
LEFT_LIMIT = 250

def publisher():
    pub = rospy.Publisher('state', Float64, queue_size=10)
    rospy.init_node('state_estimate', anonymous=True)
    rate = rospy.Rate(50)
    pololu = maestro.Controller()
    window = [0] * WINDOW_SIZE
    index = 0
    left_prev = 300
    right_prev = 300
    while not rospy.is_shutdown():
#get left ir_sensor value
        ir_left = pololu.getPosition(CHANNEL_L_IR)
        left_p = left_prev - ir_left

        if 80 < left_p < 120:
            ir_left = left_prev

        left_prev = ir_left
        dist_left = transform(ir_left)

        print 'ir left: ' + str(ir_left)
        # print 'dist left: ' + str(dist_left)

#get right ir sensor value
        ir_right = pololu.getPosition(CHANNEL_R_IR)
        right_p = right_prev - ir_right

        if 80 < right_p < 120:
            ir_right = right_prev

        right_prev = ir_right
        dist_right = transform(ir_right)
        print 'ir right: ' + str(ir_right)
        # print 'dist right: ' + str(dist_right)
        if dist_left > LEFT_LIMIT:
            dist_left = LEFT_LIMIT
        diff = dist_left - dist_right
        window[index] = diff
        index += 1
        index %= WINDOW_SIZE
        average = sum(window) / WINDOW_SIZE
        pub.publish(average)
        # print 'ir diff: ' + str(ir_left - ir_right)
        # print 'dist diff: ' + str(diff)
        # print 'average: ' + str(average)
        rate.sleep()

def myhook():
    print "shutdown time!"

rospy.on_shutdown(myhook)

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
