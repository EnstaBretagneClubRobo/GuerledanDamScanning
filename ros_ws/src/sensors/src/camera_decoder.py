#!/usr/bin/env python


# Decode the the camera feed


import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


def update_image(msg):
    global frame, bridge, flag
    print 'received'
    frame = bridge.imgmsg_to_cv2(msg, 'mono8')
    if not flag:
        flag = True


# Initiate node
rospy.init_node('video_decoder')

# Bridge object
bridge = CvBridge()

# Subscriber
sub = rospy.Subscriber('camera/image/compressed', Image, update_image)

frame = np.ndarray(0)
flag = False
print 'hello'
# Publishing the frame
while not rospy.is_shutdown():
    if flag:
        frame2 = cv2.imdecode(frame, 1)
        cv2.imshow('Image decompressed', frame2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
