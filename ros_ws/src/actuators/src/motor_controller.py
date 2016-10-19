#!/usr/bin/env python

# envoie les commandes a la polulu


import maestro
import rospy
from geometry_msgs.msg import Vector3

rospy.init_node('motors')


def set_cmd(msg):
    print 'droite {}, gauche {}'.format(msg.x, msg.y)
    servo.setTarget(0, int(msg.x))
    servo.setTarget(1, int(msg.y))


def set_param_motor():
    """ Meilleur parametres pour les moteurs (accel, speed)"""
    servo.setSpeed(0, 0)    # max = 255
    servo.setAccel(0, 0)
    servo.setSpeed(1, 150)    # max = 255
    servo.setAccel(1, 150)


def get_param(name, default):
    try:
        v = rospy.get_param(name)
        rospy.loginfo('Found parameter %s, value %s' % (name, str(v)))
    except KeyError:
        v = default
        rospy.logwarn(
            'Cannot find parameter %s, assigning default: %s' % (name, str(v)))
    return v


sPort = get_param('~sPort', '/dev/pololu')
port = get_param('~port', 0)
servo = maestro.Controller(int(port))    # faire attention au port
# servo = maestro.Controller(0, serial_port=sPort)    # faire attention au port
set_param_motor()

sub = rospy.Subscriber('cmd_diff', Vector3, set_cmd)

rospy.spin()
