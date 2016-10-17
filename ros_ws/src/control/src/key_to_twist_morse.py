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
    'z': [vmax, 0],  # avant
    'q': [0, vmax],  # gauche
    'd': [0, -vmax],  # droite
    's': [-vmax, 0],  # arriere
    ' ': [0, 0],    # stop
}


def keys_cb(msg, twist_pub):
    global speed, rot
    if len(msg.data) == 0 or msg.data not in key_mapping.keys():
        return  # nothing to do, unknown key
    vels = key_mapping[msg.data[0]]
    if msg.data == ' ':
        # we reset the speed and rot
        speed = 0
        rot = 0
    else:
        speed = vels[0]
        rot = vels[1]

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


if __name__ == '__main__':
    rospy.init_node('keys_to_twist')
    twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('keys', String, keys_cb, twist_pub)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        t = Twist()
        t.linear.x = 0
        t.angular.z = 0
        twist_pub.publish(t)
        rate.sleep()
