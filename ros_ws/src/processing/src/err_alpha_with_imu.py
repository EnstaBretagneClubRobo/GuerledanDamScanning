#!/usr/bin/env python
"""
Calcul of the distance to a line using gps, and the line coordinates
"""

import rospy
from LL_to_local import ll2local
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
import numpy as np
import tf


def calc_err_alpha(msg):
    global xs, ys, xe, ye
    alpha_wall = np.arctan2(ye - ys, xe - xs)
    q = msg.orientation
    q = [q.x, q.y, q.z, q.w]
    alpha_boat = tf.transformations.euler_from_quaternion(q)[2]
    err_cap = alpha_wall - alpha_boat
    err_cap_pub.publish(err_cap)


# Useful coordinates
center_lat = rospy.get_param('wall_center_lat', 48.00000)
center_long = rospy.get_param('wall_center_long', -3.00000)

start_lat = rospy.get_param('wall_start_lat', 48.00000)
start_long = rospy.get_param('wall_start_long', -3.000000)
ys, xs = ll2local(center_lat, center_long, start_lat, start_long)

end_lat = rospy.get_param('wall_end_lat', 48.00000)
end_long = rospy.get_param('wall_end_long', -3.000000)
ye, xe = ll2local(center_lat, center_long, end_lat, end_long)

# Init node
rospy.init_node('err_dist_calculator')

# Subscriber and publisher
gps_sub = rospy.Subscriber('imu/data', Imu, calc_err_alpha)
err_cap_pub = rospy.Publisher('err_cap', Float32, queue_size=1)

rospy.spin()
