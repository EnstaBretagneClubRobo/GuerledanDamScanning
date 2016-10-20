#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
from geometry_msgs.msg import Twist
from std_msgs import Float32
from math import atan2,pi


def update_err_cap(msg):
    global ecap
    ecap=msg.data


def update_err_d(msg):
    global eD
    eD=msg.data
    

rospy.init_node('regulation_cap')

"""
capm : orientation du mur/ligne
capd : cap désiré
capr : cap du robot

Dd : distance désirée
D : distance calculée
"""
cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
imu_sub = rospy.Subscriber('err_d', Float32, update_err_d)
cap_sub = rospy.Subscriber('err_cap', Float32, update_err_cap)


K1 = 2.5/pi
K2 = 2*(5/pi-K1)
v = 5.0
cmd = Twist()

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    cmd.angular.z = K1*ecap+K2*atan2(eD)
    if abs(eD)>1:
        cmd.linear.x = v/abs(eD)
    else :
        cmd.linear.x = v
    cmd_pub.publish(cmd)
    rate.sleep()




#imu/data
