#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

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
    if msg.data == ' ':
        # we reset the speed and rot
        speed = 0
        rot = 0
    elif msg.data == 'f':
        flag = not flag
    else:
        speed += vels[0]
        rot += vels[1]

    if speed >= 5:
        speed = 5
    elif speed <= -5:
        speed = -5
    if rot >= 5:
        rot = 5
    elif rot <= -5:
        rot = -5

    t = Twist()
    t.linear.x = speed
    t.angular.z = rot
    twist_pub.publish(t)

    # time.sleep(0.1)
    # speed = 0
    # rot = 0
    # t.linear.x = speed
    # t.angular.z = rot
    # twist_pub.publish(t)


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
        if not flag:
            speed = speed - 0.1 * sign(speed)
        rot = rot - 0.1 * sign(rot)
        t = Twist()
        t.linear.x = speed
        t.angular.z = rot
        twist_pub.publish(t)
        rate.sleep()
