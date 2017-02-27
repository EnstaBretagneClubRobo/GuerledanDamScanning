#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose2D, Twist
from regulation_imugps.msg import Segment
import numpy as np
from numpy.linalg import det, norm
from math import tan, atan, pi


# --------------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------------
def dist_droite(x, y, xa, ya, xb, yb):
    """
    Renvoie la distance d'un point (x,y) par rapport a la droite definie
     par A(xa,ya) et B(xb,yb)
    #
     distance > 0: a gauche (vers le barrage si xs est en bas)
     distance < 0: a droite
    """
    if xa == xb and ya == yb:
        return 0
    ab = np.array([xb - xa, yb - ya])
    am = np.array([x - xa, y - ya])
    e = det([ab / norm(ab), am])
    return e


# --------------------------------------------------------------------------------
# Node init
# --------------------------------------------------------------------------------
rospy.init_node('line_following')


# --------------------------------------------------------------------------------
# Subscribe to a pose2D
# --------------------------------------------------------------------------------
def update_pose(msg):
    global pose
    pose = msg


pose_sub = rospy.Subscriber('car/pose', Pose2D, update_pose)
pose = Pose2D()


# --------------------------------------------------------------------------------
# Subscribe to the line to follow
# --------------------------------------------------------------------------------
def update_line(msg):
    global line
    line = msg


line_sub = rospy.Subscriber('line', Segment, update_line)
line = Segment()

# --------------------------------------------------------------------------------
# Publisher for the command
# --------------------------------------------------------------------------------
cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
cmd = Twist()


# --------------------------------------------------------------------------------
# Parameter of the simulation
# --------------------------------------------------------------------------------
rate = rospy.Rate(10)
K = 10 / pi     # rad/s
radius = 5      # largeur d'effet du suivi de ligne


# --------------------------------------------------------------------------------
# LOOP
# --------------------------------------------------------------------------------

while not rospy.is_shutdown():
    # Wall direction
    dy = line.exit.y - line.entry.y
    dx = line.exit.x - line.entry.x
    line_dir = np.arctan2(dy, dx)
    # Direction of the boat relatively to the wall direction
    boat_wdir = line_dir - pose.theta
    # Distance to the line:
    dist2line = dist_droite(pose.x, pose.y, line.entry.x,
                            line.entry.y, line.exit.x, line.exit.y)

    # Heading error:
    h_err = boat_wdir - atan(dist2line / radius)
    h_err = h_err / 2   # pour ramener de [-pi,pi] a [-pi/2,pi/2]
    cmd.angular.z = K * atan(tan((h_err)))
    cmd.linear.x = 10

    cmd_pub.publish(cmd)
    # DEBUG
    log = 'line_dir: {}\ttheta: {}\tboat_wdir:{}\tdist2line: {}'
    log += '\tangular: {}\tlinear: {}'
    print log.format(line_dir, pose.theta, boat_wdir,
                     dist2line, cmd.angular.z, cmd.linear.x)

    if (pose.x-line.exit.x)*(line.entry.x-line.exit.x) + (pose.y-line.exit.y)*(line.entry.y-line.exit.y) < 0:
        print 'fuck'

    rate.sleep()
