#!/usr/bin/env python
import rospy
from models import Car
from geometry_msgs.msg import Twist

rospy.init_node('sim_car')

# --------------------------------------------------------------------------------
# Car
# --------------------------------------------------------------------------------
car = Car()


# --------------------------------------------------------------------------------
# Subscribe to cmd
# --------------------------------------------------------------------------------
def update_cmd(msg):
    global cmd
    cmd = msg


sub = rospy.Subscriber('cmd_vel', Twist, update_cmd)

# --------------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------------
rate = rospy.Rate(10)
cmd = Twist()

while not rospy.is_shutdown():
    car.simulate(cmd.linear.x, cmd.angular.z)
    print 'Car position: {}, {}, {}'.format(car.x, car.y, car.theta)
    rate.sleep()
