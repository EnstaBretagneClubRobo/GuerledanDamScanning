#!/usr/bin/env python
"""
Calcul of the distance to a line using gps, and the line coordinates
"""

import rospy
from LL_to_local import ll2local
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float32
import numpy as np
from numpy.linalg import det
from numpy.linalg import norm


def calc_dist(msg):
    global xs, ys, xe, ye, desired_distance_to_wall
    # Coordinate of the boat in the frame centered on wall_center
    y, x = ll2local(center_lat, center_long, msg.latitude, msg.longitude)
    err_d = dist_droite(x, y, xs, ys, xe, ye) + desired_distance_to_wall
    err_d_pub.publish(err_d)


def dist_droite(x, y, xa, ya, xb, yb):
    """
    Renvoie la distance d'un point (x,y) par rapport a la droite definie
     par A(xa,ya) et B(xb,yb)
    """
    if xa == xb and ya == yb:
        return 0
    ab = np.array([xb - xa, yb - ya])
    am = np.array([x - xa, y - ya])
    e = det([ab / norm(ab), am])
    return e


# Useful coordinates
center_lat = rospy.get_param('~wall_center_lat', 48.19513)
center_long = rospy.get_param('~wall_center_long', -3.01798)

start_lat = rospy.get_param('~wall_start_lat', 48.194260)
start_long = rospy.get_param('~wall_start_long', -3.017179)
ys, xs = ll2local(center_lat, center_long, start_lat, start_long)

end_lat = rospy.get_param('~wall_end_lat', 48.195344)
end_long = rospy.get_param('~wall_end_long', -3.018396)
ye, xe = ll2local(center_lat, center_long, end_lat, end_long)

desired_distance_to_wall = rospy.get_param('~required_wall_dist', 4)

rospy.init_node('err_dist_calculator')

gps_sub = rospy.Subscriber('gps', NavSatFix, calc_dist)
err_d_pub = rospy.Publisher('err_d', Float32, queue_size=1)

rospy.spin()
