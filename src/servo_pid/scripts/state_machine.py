#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import Float64

rospy.init_node('state_machine', anonymous=True)

global rate = rospy.rate(50)

# create publisher object and map to "control_pub" variable. Publish to "/control_input"
# topic which the pololupub.py subscribes to.
control_pub = rospy.Publisher('control_input', Float64, queue_size=10)

# State input from IR sensor, data in is average distance from center of hallway
# Negative value = Left of Center
# Positive value = Right of Center


#Going State State
class Straight(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['corner'])

        #Pull state information from state_publisher, in form of distance from center in cm
        self.ir_in = rospy.Subscriber('state', Float64, queue_size=10)
        self.ce_straight = rospy.Subscriber('ce_straight', Float64, queue_size=10)

    def execute(self, userdata):
        #rospy.loginfo('Straight')
        if self.ir_in > 200:
            return 'corner'
        else
            control_pub.publish(ce_straight)
            rospy.sleep(rate)
            print('FULL SPEED AHEAD!')

#Going around a corner state
class Corner(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['straight'])

        #Pyll state information form state_publisher, in form of distance from center in cm
        self.ir_in = rospy.Subscriber('state', Float64, queue_size=10)
        self.ce_corner = rospy.Subscriber('ce_corner', Float64, queue_size=10)

    def execute(self, userdata):
        #rospy.loginfo('Corner')
        if 75 < ir_in:
            control_pub.publish(ce_corner)
            rospy.sleep(rate)
            print('CORNERING!')
        else
            return 'straight'

def main():
    #Create State SMACH state machine
    sm = smach.StateMachine(outcomes=['base'])

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
