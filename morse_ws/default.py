#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <morse_ws> environment

Feel free to edit this template as you like!
"""
from morse.builder import *
from math import pi

# #############################################################################
#
# ROBOT
#
# #############################################################################
robot = ATRV()
robot.translate(1.0, 0.0, 3.0)
robot.rotate(0.0, 0.0, 0.)

# #############################################################################
#
# Motion Controller
#
# #############################################################################
motion = MotionVW()
motion.add_stream('ros')
robot.append(motion)


# #############################################################################
#
# Keyboard Controller
#
# #############################################################################
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(Speed=4, ControlType='Position')

# #############################################################################
#
# Sensors
#
# #############################################################################

# Pose ------------------------------------------------------------------------
pose = Pose()
robot.append(pose)
pose.add_stream('ros')

# Hokuyo Sensor ---------------------------------------------------------------
hokuyo = Hokuyo()
hokuyo.translate(0, 0, 1)
hokuyo.rotate(0, 0, pi / 2)
# Properties
# (https://www.hokuyo-aut.jp/02sensor/07scanner/urg_04lx_ug01.html)
# 2cm to 5.6m | 240d |
# Accuracy ±30mm (6cm<o<1m)
# Accuracy 0.3% (1m<o<4.095m)
hokuyo.properties(laser_range=5.6)
hokuyo.properties(resolution=0.36)
hokuyo.properties(scan_window=240.0)
# hokuyo.properties(Visible_arc=True)   # slows down simulation

hokuyo.add_stream('ros')
robot.append(hokuyo)

# Imu -------------------------------------------------------------------------
imu = IMU()
imu.translate(0, 0, 0)
imu.rotate(0, 0, 0)
imu.add_stream('ros')
robot.append(imu)

# Camera ----------------------------------------------------------------------
videocamera = VideoCamera()
videocamera.translate(0, 0, 1.5)
videocamera.rotate(pi / 2, 0., 0.)
# Properties
videocamera.properties(cam_width=256, cam_height=256)
videocamera.add_stream('ros')
robot.append(videocamera)


# #############################################################################
#
# For debugging ?
#
# #############################################################################
# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')

# #############################################################################
#
# Environment
#
# #############################################################################
# PATH
project_path = '/Users/ejalaa/Documents/Projects/GuerledanDamScanning/Git_GuerledanDamScanning/'
env_folder = 'morse_ws/environments/'
file = 'outdoors_flat_empty.blend'
# ENVIRONMENT
env = Environment(project_path + env_folder + file, fastmode=False)
env.set_camera_location([-36.0, -15, 30])
env.set_camera_rotation([1.09, 0, -1.14])
# Properties for magnetomer in IMU
env.properties(longitude=1.26, latitude=43.26, altitude=130.0)
