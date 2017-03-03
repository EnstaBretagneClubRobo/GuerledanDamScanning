#!/usr/bin/env python


# conversion lat/long vers local
# renvoie l orientation du robot
# Lat Long - UTM, UTM - Lat Long conversions

import rospy
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import PoseStamped, Pose2D
from math import pi, cos
from tf.transformations import euler_from_quaternion

# Point Reperable

LAT0 = 48.418042    # lab ensta
LON0 = -4.472227
R = 6371000

# terrain de foot
# 48.418345, -4.473892


def deg2rad(deg):
    return deg * pi / 180


def ll2local(lat0, lon0, lat, lon):
    R = 6371000
    x = R * deg2rad(lat - lat0)
    y = R * cos(deg2rad(lat)) * deg2rad(lon - lon0)
    # x pointe vers le nord et y vers l'est et z vers le bas
    return [x, y]


def update_pose(msg):
    global pos, pose2d
    # on inverse en mettant z vers le haut donc x=y et y=x
    y, x = ll2local(LAT0, LON0, msg.latitude, msg.longitude)
    print x, y

    # update pose stamped
    pos.header.stamp = rospy.Time.now()
    pos.pose.position.x = x
    pos.pose.position.y = y
    pos.pose.position.z = 0
    # update pose 2d
    pose2d.x = x
    pose2d.y = y


def update_orientation(msg):
    global pos
    # update pose stamped
    pos.header.stamp = rospy.Time.now()
    pos.pose.orientation = msg.orientation
    # update pose 2d
    q = msg.orientation
    pose2d.theta = euler_from_quaternion([q.x, q.y, q.z, q.w])[2]
    # offset to put 0 to east
    pose2d.theta += pi / 2


if __name__ == '__main__':
    rospy.init_node('Local_publisher')

    sub_gps = rospy.Subscriber('gps', NavSatFix, update_pose)
    sub_imu = rospy.Subscriber('imu/data', Imu, update_orientation)
    pub_stamped = rospy.Publisher(
        'gps/local_pose_stamped', PoseStamped, queue_size=1)
    pub_2d = rospy.Publisher('gps/local_pose', Pose2D, queue_size=1)

    # PoseStamped
    pos = PoseStamped()
    pos.header.frame_id = 'world'
    # Pose2D
    pose2d = Pose2D()
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        pos.header.stamp = rospy.Time.now()
        pub_stamped.publish(pos)
        pub_2d.publish(pose2d)
        rate.sleep()
