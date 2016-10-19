#!/usr/bin/env python


# Read & Compress & Publish the camera feed


import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError


def get_param(name, default):
    try:
        v = rospy.get_param(name)
        rospy.loginfo('Found parameter %s, value %s' % (name, str(v)))
    except KeyError:
        v = default
        rospy.logwarn(
            'Cannot find parameter %s, assigning default: %s' % (name, str(v)))
    return v


# Initiate node
rospy.init_node('video_capture')

# Node rate
rate = rospy.Rate(10)

# Camera path
cam_path = get_param('~campath', '/dev/camera')
print cam_path

# Bridge object
bridge = CvBridge()

# Publisher
pub = rospy.Publisher('camera/image/compressed', Image, queue_size=1)
# Capture object
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print 'Error while opening: ' + cam_path
    exit(0)
else:
    print 'Correctly opened ' + cam_path

# Publishing the frame
rval, frame = cap.read()
while rval and not rospy.is_shutdown():
    rval, frame = cap.read()
    print frame.shape
    retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    try:
        pub.publish(bridge.cv2_to_imgmsg(frame, "mono8"))
        # cv2.imdecode(frame2,1) a rajouter en sortie
    except CvBridgeError as e:
        print e
    rate.sleep()
