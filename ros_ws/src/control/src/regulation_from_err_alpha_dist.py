#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
from math import atan, pi
import tf


def update_err_d(msg):
    global eD
    eD = msg.data

def update_err_d(msg):
    global eD
    eD = msg.data


rospy.init_node('regulation_cap')

"""
capm : orientation du mur/ligne
capd : cap desire
capr : cap du robot

Dd : distance desiree
D : distance calculee
"""
cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
imu_sub = rospy.Subscriber('err_d', Float32, update_err_d)
gps_sub = rospy.Subscriber('imu/data', Imu, update_heading)


headingR, eD = 0, 0

K = 10 / pi
v = 5.0
cmd = Twist()

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    cmd.angular.z = - K1 * ecap + K2 * atan(eD)
    cmd.linear.x = v
    # if abs(eD) > 1:
    #     cmd.linear.x = v / abs(eD)
    # else:
    #     cmd.linear.x = v
    cmd_pub.publish(cmd)
    rate.sleep()


# imu/data
