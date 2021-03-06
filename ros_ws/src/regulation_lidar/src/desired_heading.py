#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
import tf
from geometry_msgs.msg import Twist, Quaternion
from std_msgs.msg import Float32
from sensor_msgs import Imu


def update_dist(msg):
    global D
    D = msg.data - Dd


def update_cap(msg):
    global capm
    capm = msg.data


rospy.init_node('desired_heading')

"""
capm : orientation du mur/ligne
capd : cap désiré
capr : cap du robot

Dd : distance désirée
D : distance calculée
"""
dist_sub = rospy.Subscriber('wall_dist', Float32, update_dist)
cap_sub = rospy.Subscriber('wall_cap', Float32, update_cap)
cap_pub = rospy.Publisher('cap_des', Float32, queue_size=1)

if D < -1.0:
    D = -1.0
elif D > 1.0:
    D = 1.0
K = 2.0
capd = capm + K * D


rate = rospy.Rate(1)
while not rospy.is_shutdown():
    cap_pub.publish(capd)
    rate.sleep()
