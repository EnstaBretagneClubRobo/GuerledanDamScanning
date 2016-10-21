#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
import tf
from geometry_msgs.msg import Twist, Quaternion
from std_msgs import Float32
from sensor_msgs import Imu


def update_cmd(msg):
    global cmd
    error = msg.data - 4
    K = 0.1
    cmd.angular.z = K * error
    print msg.data, K * error


def update_cap_des(msg)
    global capm
    capd = msg.data


def update_imu(msg)
    global capr
    Qr = Quaternion()
    Qr = msg.data
    capr = tf.transformations.euler_from_quaternion(Qr)[2]


rospy.init_node('regulation_cap')

"""
capm : orientation du mur/ligne
capd : cap désiré
capr : cap du robot

Dd : distance désirée
D : distance calculée
"""
Dd = 4
K = -3.14 / 2
cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
imu_sub = rospy.Subscriber('imu/data', Imu, update_imu)
cap_sub = rospy.Subscriber('cap_des', Float32, update_cap_des)


cmd = Twist()
cmd.angular.z = capd - capr
cmd.linear.x = v

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    cmd_pub.publish(Qd)
    rate.sleep()


# imu/data
