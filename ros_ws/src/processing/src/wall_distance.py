#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32


def calcul_wall_dist(msg):
    print min(msg.ranges)
    dist_pub.publish(min(msg.ranges))


rospy.init_node('calcul_wall_distance')

scan_sub = rospy.Subscriber('scan', LaserScan, calcul_wall_dist)
dist_pub = rospy.Publisher('wall_dist', Float32, queue_size=1)

rospy.spin()
