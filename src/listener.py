import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def listener():
    rospy.init_node("image",anonymous = True)
    rospy.Subscriber("/camera/image_raw",Image,callback, queue_size=1)
    rospy.spin()

def callback(data):
    try:
        cv_image = CvBridge().imgmsg_to_cv2(data)
    except CvBridgeError as e:
        print e

    cv2.imshow("1", cv_image)
    cv2.waitKey(1)

if __name__ == '__main__':
    listener()
