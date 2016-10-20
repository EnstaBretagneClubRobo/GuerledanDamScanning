#!/usr/bin/env python


# publie la transformee entre 2 frames


import rospy
import tf
from sensor_msgs.msg import TimeReference
from math import radians


def update_time(msg):
    global time
    time = msg.header.stamp
    print time


rospy.init_node('laser_2_boat_tf')

sub_time = rospy.Subscriber('/time_reference', TimeReference, update_time)

br = tf.TransformBroadcaster()
rate = rospy.Rate(20)
heading = 0
time = 0
while not rospy.is_shutdown():
    r = tf.transformations.quaternion_from_euler(0, 0, radians(180))
    br.sendTransform((0, 0, 0),
                     (r[0], r[1], r[2], r[3]),
                     time,
                     rospy.get_param('~frame1', 'laser'),
                     rospy.get_param('~frame0', 'boat'))
    rate.sleep()
