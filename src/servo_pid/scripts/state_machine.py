#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64

rospy.init_node('state_machine', anonymous=True)

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

        rospy.Subscriber('state', Float64, callback)
        #Pull state information from state_publisher, in form of distance from center in cm

    def execute(self, userdata):
        #rospy.loginfo('Straight')
        if userdata.ir_in > 200:
            return 'corner'
        else:
            rospy.Subscriber('ce_straight', Float64, cb_straight)
            rospy.Subscriber('state', Float64, callback)
            control_pub.publish(userdata.ce_straight)
            rate.sleep()
            print('FULL SPEED AHEAD!')


#Going around a corner state
class Corner(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                                outcomes=['straight'],
                                input_keys=['ir_in', 'ce_corner'])

        #Pyll state information form state_publisher, in form of distance from center in cm
        rospy.Subscriber('ce_corner', Float64, cb_corner)

    def execute(self, userdata):
        #rospy.loginfo('Corner')
        if 75 < userdata.ir_in:
            rospy.Subscriber('ce_corner', Float64, cb_corner)
            rospy.Subscriber('state', Float64, callback)
            control_pub.publish(userdata.ce_corner)
            rate.sleep()
            print('CORNERING!')
        else:
            return 'straight'

def callback(data):
    userdata.ir_in = data.data
    return userdata

def cb_straight(data):
    userdata.ce_straight = data.data
    return  userdata

def cb_corner(data):
    userdata.ce_corner = data.data
    return userdata

def main():
    #Create State SMACH state machine
    sm = smach.StateMachine(outcomes=['base'])
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
