import roslib

#roslib.load_manifest('video_stream_opencv')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
import numpy as np
import darknet as dn
#from PIL import Image, ImageDraw, ImageFont


dn.set_gpu(0)
meta = dn.load_meta("cfg/coco.data")

net = dn.load_net("cfg/yolov2-tiny.cfg",
                  "yolov2-tiny.weights",0)
i_image = 0


def generate_colors(num_classes):
    global box_colors

    if box_colors != None and len(box_colors) > num_classes:
        return box_colors

    hsv_tuples = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    box_colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    box_colors = list(
        map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
            box_colors))
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    # Shuffle colors to decorrelate adjacent classes.
    random.shuffle(box_colors)
    random.seed(None)  # Reset seed to default.


def draw_boxes(img, result):

    image = Image.fromarray(img)

    font = ImageFont.truetype(font='font/FiraMono-Medium.otf', size=20)
    thickness = (image.size[0] + image.size[1]) // 300

    num_classes = len(result)
    generate_colors(num_classes)

    index = 0
    for objection in result:
        index += 1
        class_name, class_score, (x, y, w, h) = objection
        print(name, score, x, y, w, h)

        left = int(x - w / 2)
        right = int(x + w / 2)
        top = int(y - h / 2)
        bottom = int(y + h / 2)

        label = '{} {:.2f}'.format(class_name.decode('utf-8'), class_score)

        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label, font)

        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
        print(label, (left, top), (right, bottom))

        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i,
                            bottom - i], outline=box_colors[index - 1])
        draw.rectangle(
            [tuple(text_origin), tuple(text_origin + label_size)],
            fill=box_colors[index - 1])
        draw.text(text_origin, label, fill=(255, 255, 255), font=font)
        del draw

    return np.array(image)



def listener():

    rospy.init_node('image_converter',anonymous = True)
    #rate = rospy.Rate(0.1)
    
    
    #rospy.Subscriber("/camera/image_raw", Image, callback)
    rospy.Subscriber("/camera/image_raw", Image, callback)
    rospy.sleep(10)

    rospy.spin()
    


def callback(data):

    try:
        
        cv_image = CvBridge().imgmsg_to_cv2(data,'bgr8')

	#cv_image = cv2.resize(cv_image, (0, 0), fx=0.5, fy=0.5) 

	#input_image = array_to_image(cv_image)

        #image = dn.rgbgr_image(cv_image)
	
        if i_image%10 == 0:
            img_name = "frame"+str(i_image)+".jpg"
	    cv2.imwrite(img_name, cv_image) 
            #img = cv2.imread("frame.jpg",0)
            print(i_image)
            #res= dn.detect(net, meta, "frame.jpg")
            #print("i detect")

        global i_image
        i_image += 1
	#index = 0
    	#for objection in res:
      	#  index += 1
      	#  class_name, class_score, (x, y, w, h) = objection
        #print(res)
        
        #out_img = draw_boxes("data/dog.jpg", detection)

        #cv2.imshow("yolo", img)


    except CvBridgeError as e:
        print(e)


    cv2.waitKey(3)


if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()



