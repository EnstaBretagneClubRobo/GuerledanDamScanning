#!/usr/bin/env python


# conversion lat/long vers local
# renvoie l orientation du robot
# Lat Long - UTM, UTM - Lat Long conversions

import rospy
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import PoseStamped
from math import pi, cos

# Point Reperable

LAT0 = 48.1949716667    # Debut du log gps001 du bateau
LON0 = -3.01758666667
R = 6371000


def deg2rad(deg):
    return deg * pi / 180


def ll2local(lat0, lon0, lat, lon, rho):
    x = rho * deg2rad(lat - lat0)
    y = rho * cos(deg2rad(lat)) * deg2rad(lon - lon0)
    return [x, y]


def update_pose(msg):
    global pos
    y, x = ll2local(LAT0, LON0, msg.latitude, msg.longitude, R)
    print x, y

    pos.header.stamp = rospy.Time.now()
    pos.pose.position.x = x
    pos.pose.position.y = y
    pos.pose.position.z = 0


def update_orientation(msg):
    global pos
    pos.header.stamp = rospy.Time.now()
    pos.pose.orientation = msg.orientation


rospy.init_node('Local_publisher')

sub_gps = rospy.Subscriber('gps', NavSatFix, update_pose)
sub_imu = rospy.Subscriber('imu/data', Imu, update_orientation)
pub = rospy.Publisher('gps/local_pose', PoseStamped, queue_size=1)

pos = PoseStamped()
pos.header.frame_id = 'world'
rate = rospy.Rate(50)

while not rospy.is_shutdown():
    pos.header.stamp = rospy.Time.now()
    pub.publish(pos)
    rate.sleep()
