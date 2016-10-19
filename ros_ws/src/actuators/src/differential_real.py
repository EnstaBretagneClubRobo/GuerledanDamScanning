#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Vector3


def update_cmd(msg):
    L = 400.
    om = msg.angular.z
    v = 6000 - 200. * msg.linear.x
    print v, om
    vd = v + om * L / 2.0
    vg = v - om * L / 2.0
    cmd = Vector3()
    cmd.x = vd
    cmd.y = vg
    cmd_pub.publish(cmd)


rospy.init_node('differential')
dist_sub = rospy.Subscriber('cmd_vel', Twist, update_cmd)
cmd_pub = rospy.Publisher('cmd_diff', Vector3, queue_size=1)
rospy.spin()
