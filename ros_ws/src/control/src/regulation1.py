#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


def update_cmd(msg):
    global cmd
    error = msg.data - 4
    K = 0.1
    cmd.angular.z = K * error
    print msg.data, K * error
    # if msg.data > 4:
    # else:
    #     cmd.angular.z = -0.2 * error


rospy.init_node('regulation1')

dist_sub = rospy.Subscriber('wall_dist', Float32, update_cmd)
cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

cmd = Twist()
cmd.linear.x = 2

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    cmd_pub.publish(cmd)
    rate.sleep()
