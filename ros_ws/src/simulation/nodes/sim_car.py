#!/usr/bin/env python
import rospy
from models import Car
from geometry_msgs.msg import Twist
import matplotlib.pyplot as plt

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
# plt.ion()

while not rospy.is_shutdown():
    plt.clf()

    car.simulate(cmd.linear.x, cmd.angular.z)
    img = car.draw()
    plt.plot(img[0], img[1])
    plt.axis([car.x - 50, car.x + 50, car.y - 50, car.y + 50])
    print 'Car position: {}, {}, {}'.format(car.x, car.y, car.theta)
    plt.pause(rate.sleep_dur.to_sec())
    rate.sleep()
