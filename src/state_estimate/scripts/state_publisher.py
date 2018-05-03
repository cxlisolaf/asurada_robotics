#!/usr/bin/env python
import maestro
import rospy
from std_msgs.msg import Float64
from transform import transform

CHANNEL_L_IR = 6
CHANNEL_R_IR = 11
WINDOW_SIZE = 10
LEFT_LIMIT = 250
RIGHT_LIMIT = 250
RIGHT_LIMIT_DOOR = 100
LEFT_LIMIT_DOOR = 100
LEFT_LIMIT_TURN = 400

def publisher():
    pub = rospy.Publisher('state', Float64, queue_size=10)
    right_pub = rospy.Publisher('dist_right', Float64, queue_size=10)
    left_pub = rospy.Publisher('dist_left', Float64, queue_size=10)
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

#        if 80 < left_p < 120:
#            ir_left = left_prev

        left_prev = ir_left
        dist_left = transform(ir_left)

#        rospy.loginfo('ir left: ' + str(ir_left))
        # print 'dist left: ' + str(dist_left)

#get right ir sensor value
        ir_right = pololu.getPosition(CHANNEL_R_IR)
        right_p = right_prev - ir_right

#        if 80 < right_p < 120:
#            ir_right = right_prev

        right_prev = ir_right
        dist_right = transform(ir_right)
#        rospy.loginfo('ir right: ' + str(ir_right))
        # print 'dist right: ' + str(dist_right)
#        if dist_left < 250 and dist_right < 250:
#            pass
        if dist_left < LEFT_LIMIT_TURN and dist_right > 200:
            pass
        elif dist_left > LEFT_LIMIT and dist_right < 250:
            dist_left = LEFT_LIMIT
            rospy.loginfo('LEFT LIMIT')
        elif dist_left > LEFT_LIMIT_DOOR and dist_right > RIGHT_LIMIT_DOOR:
            dist_left = LEFT_LIMIT
            dist_right = RIGHT_LIMIT
            rospy.loginfo('DOOR IGNORE')
#        elif dist_left > LEFT_LIMIT and dist_right > 250:
#            rospy.loginfo('LEFT LIMIT')

        diff = dist_left - dist_right
        window[index] = diff
        index += 1
        index %= WINDOW_SIZE
        average = sum(window) / WINDOW_SIZE
        pub.publish(average)
        right_pub.publish(dist_right)
        left_pub.publish(dist_left)
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
