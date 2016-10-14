#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('regulation')

cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

cmd = Twist()
cmd.linear.x = 0.5

rate = rospy.Rate(1)

while not rospy.is_shutdown():
    cmd_pub.publish(cmd)
    rate.sleep()
