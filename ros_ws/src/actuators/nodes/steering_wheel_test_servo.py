#!/usr/bin/env python
import rospy
from helpers import maestro
from geometry_msgs.msg import Twist

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
    print msg.angular.z
    servo.setTarget(5, int(msg.angular.z))


sub = rospy.Subscriber('cmd_vel', Twist, cmd_servo)

rospy.spin()
