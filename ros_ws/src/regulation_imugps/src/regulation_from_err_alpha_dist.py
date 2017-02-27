#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from math import atan, pi, tan


def update_err_d(msg):
    global eD
    eD = msg.data


def update_err_cap(msg):
    global ecap
    ecap = msg.data


rospy.init_node('regulation_cap')

cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
imu_sub = rospy.Subscriber('err_d', Float32, update_err_d)
gps_sub = rospy.Subscriber('err_cap', Float32, update_err_cap)

# erreur en cap et en distance
ecap, eD = 0, 0

K = -3 / pi     # rad/s
radius = 5      # largeur d'effet du suivi de ligne
v = -5.0        # todo trouver pourquoi
cmd = Twist()

rate = rospy.Rate(20)   # il faut avoir une bonne frequence

while not rospy.is_shutdown():
    err = ecap - atan(eD / radius)
    err = err / 2   # pour ramener de [-pi,pi] a [-pi/2,pi/2]
    cmd.angular.z = K * atan(tan((err)))
    print ecap, atan(eD)
    cmd.linear.x = v
    cmd_pub.publish(cmd)
    rate.sleep()
