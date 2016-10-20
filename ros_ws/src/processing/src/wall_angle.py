#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
import numpy as np


def calcul_wall_dist(msg):
    # ranges[0] corresponds to the front of the car
    ranges = np.array(msg.ranges)
    # Generate the angles corresponding to each range
    thetas = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment)

    # Calculate the position of each range returned in the lidar frame
    # Lidar frame (x heads to the center of the arc)
    xi = ranges * np.cos(thetas)
    yi = ranges * np.sin(thetas)
    # Then transform in the frame of the robot
    x = -xi
    y = -yi
    # Remove all point where the lidar didn't catch anything
    xf = x[ranges < 5.599]
    yf = y[ranges < 5.599]

    # calculate the angle of the wall
    alpha = np.arctan2(yf[-1] - yf[0], xf[-1] - xf[0])
    print alpha
    # alpha < 0 ==> has to go left to be in front of the wall
    # alpha > 0 ==> has to go right to be in front of the wall
    pts_pub.publish(alpha)


rospy.init_node('calcul_wall_cap')

scan_sub = rospy.Subscriber('scan', LaserScan, calcul_wall_dist)
pts_pub = rospy.Publisher('wall_cap', Float32, queue_size=1)


rospy.spin()
