#!/usr/bin/env python
import rospy
from helpers import maestro
from geometry_msgs.msg import Twist
from math import pi

# --------------------------------------------------------------------------------
# Initialisation du noeud
# --------------------------------------------------------------------------------
rospy.init_node('steering_wheel_command')

# --------------------------------------------------------------------------------
# Maestro Controller
# --------------------------------------------------------------------------------
servo = maestro.Controller()


# --------------------------------------------------------------------------------
# Subscribe to the command
# --------------------------------------------------------------------------------

def cmd_servo(msg):
    global servo
    # les commandes sont comprises entre -pi/2 et pi/2
    # donc on les ramene a 4000;8000]
    cmd = 6000 + msg.angular.z * 4000 / pi
    print msg.angular.z, int(cmd)
    servo.setTarget(5, int(cmd))


sub = rospy.Subscriber('cmd_vel', Twist, cmd_servo)

rospy.spin()
