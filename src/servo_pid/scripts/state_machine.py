#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64

rospy.init_node('state_machine', anonymous=True)
global control_pub
global rate
rate = rospy.Rate(50) #in Hz

# create publisher object and map to "control_pub" variable. Publish to "/control_input"
# topic which the pololupub.py subscribes to.
control_pub = rospy.Publisher('control_input', Float64, queue_size=10)

# State input from IR sensor, data in is average distance from center of hallway
# Negative value = Left of Center
# Positive value = Right of Center

#Going State State
class Straight(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                                outcomes=['corner'],
                                input_keys=['ir_in', 'ce_straight'])

    def execute(self, userdata):
        #rospy.loginfo('Straight')
        while userdata.ir_in < 200:
            rospy.Subscriber('ce_straight', Float64, self.cb_straight)
            rospy.Subscriber('state', Float64, self.callback)
            control_pub.publish(userdata.ce_straight)
            rate.sleep()
#            print('FULL SPEED AHEAD!')
        else:
            return 'corner'

    def callback(self, data):
        userdata.ir_in = data.data
        rospy.loginfo('Got ir_in callback')

    def cb_straight(self, data):
        rospy.loginfo('Got ce_straight callback')
        userdata.ce_straight = data.data

#        if userdata.ir_in > 200:
#            return 'corner'
#        else:
#            rospy.Subscriber('ce_straight', Float64, cb_straight)
#            rospy.Subscriber('state', Float64, callback)
#            control_pub.publish(userdata.ce_straight)
#            rate.sleep()
#            print('FULL SPEED AHEAD!')
#            return 'straight'


#Going around a corner state
class Corner(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                                outcomes=['straight'],
                                input_keys=['ir_in', 'ce_corner'])

    def execute(self, userdata):
        #rospy.loginfo('Corner')
        while userdata.ir_in > 75:
            rospy.Subscriber('ce_corner', Float64, self.cb_corner)
    #        rospy.Subscriber('state', Float64, callback)
            control_pub.publish(userdata.ce_corner)
            rate.sleep()
#            print('CORNERING!')
        else:
            return 'straight'

#    def callback(data):
#        userdata.ir_in = data.data
#        rospy.loginfo('Got ir_in callback')

    def cb_corner(data):
        rospy.loginfo('Got ce_corner callback')
        userdata.ce_corner = data.data

#        if 75 < userdata.ir_in:
#            rospy.Subscriber('ce_corner', Float64, cb_corner)
#            rospy.Subscriber('state', Float64, callback)
#            control_pub.publish(userdata.ce_corner)
#            rate.sleep()
#            print('CORNERING!')
#            return 'corner'
#        else:
#            return 'straight'


def main():
    #Create State SMACH state machine
    sm = smach.StateMachine(outcomes=['BASE'])
    sm.userdata.ir_in = 0 #initialize userdata object with attribute ir_in at 0
    sm.userdata.ce_corner = 0
    sm.userdata.ce_straight = 0

    #Open the State container here
    with sm:
        #Add States with transitions
        smach.StateMachine.add('STRAIGHT', Straight(),
                                transitions={'corner':'CORNER'})
        smach.StateMachine.add('CORNER', Corner(),
                                transitions={'straight':'STRAIGHT'})

    outcome = sm.execute()



if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
