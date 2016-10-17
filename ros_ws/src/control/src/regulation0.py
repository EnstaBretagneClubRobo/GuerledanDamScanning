#!/usr/bin/env python
"""
This regulateur is just a template and publish a forward command only
"""
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('regulation0')

cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

cmd = Twist()
cmd.linear.x = 2

rate = rospy.Rate(1)

while not rospy.is_shutdown():
    cmd_pub.publish(cmd)
    rate.sleep()
