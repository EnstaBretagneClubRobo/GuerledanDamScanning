#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from math import pi

# Middle speed and rotations
speed = 0
rot = 0
vmax = 5
rotmax = 5

key_mapping = {
    'w': [0.1, 0],  # avant
    'a': [0, 0.1],  # gauche
    'd': [0, -0.1],  # droite
    's': [-0.1, 0],  # arriere
    ' ': [0, 0],    # stop
    'f': [1, 1]     # flag
}


def keys_cb(msg, twist_pub):
    global speed, rot, flag
    if len(msg.data) == 0 or msg.data not in key_mapping.keys():
        return  # nothing to do, unknown key
    vels = key_mapping[msg.data[0]]
    speed += vels[0]
    rot += vels[1]

    if speed >= pi / 2:
        speed = pi / 2
    elif speed <= -pi / 2:
        speed = -pi / 2
    if rot >= pi / 2:
        rot = pi / 2
    elif rot <= -pi / 2:
        rot = -pi / 2

    t = Twist()
    t.linear.x = speed
    t.angular.z = rot
    twist_pub.publish(t)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


if __name__ == '__main__':
    rospy.init_node('keys_to_twist')
    twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('keys', String, keys_cb, twist_pub)
    rate = rospy.Rate(5)
    flag = False
    while not rospy.is_shutdown():
        t = Twist()
        t.linear.x = speed
        t.angular.z = rot
        twist_pub.publish(t)
        rate.sleep()
