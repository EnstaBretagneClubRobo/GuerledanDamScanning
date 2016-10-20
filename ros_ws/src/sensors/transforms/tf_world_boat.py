#!/usr/bin/env python


# publie la transformee entre 2 frames


import rospy
import tf
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import Quaternion
from math import radians, cos

LAT0 = 48.1949716667    # Debut du log gps001 du bateau
LON0 = -3.01758666667
R = 6371000


def ll2local(lat0, lon0, lat, lon, rho):
    x = rho * radians(lat - lat0)
    y = rho * cos(radians(lat)) * radians(lon - lon0)
    return [x, y]


def update_pose(msg):
    global x, y, z, time
    y, x = ll2local(LAT0, LON0, msg.latitude, msg.longitude, R)
    z = msg.altitude - 165
    time = msg.header.stamp
    print x, y, z, time


def update_orientation(msg):
    global thetas
    thetas = msg.orientation


rospy.init_node('boat_2_world_tf')

sub_gps = rospy.Subscriber('gps', NavSatFix, update_pose)
sub_imu = rospy.Subscriber('imu/data', Imu, update_orientation)


br = tf.TransformBroadcaster()
rate = rospy.Rate(20)
heading = 0
x, y, z, thetas, time = 0, 0, 0, Quaternion(), 0
while not rospy.is_shutdown():
    br.sendTransform((x, y, z),
                     (thetas.x, thetas.y, thetas.z, thetas.w),
                     time,
                     rospy.get_param('~frame1', 'boat'),
                     rospy.get_param('~frame0', 'world'))
    rate.sleep()
