#!/usr/bin/env python
import rospy
from models import Car
from geometry_msgs.msg import Twist, Pose2D
import matplotlib.pyplot as plt
from regulation_imugps.msg import Segment

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
# Subscribe to the line
# --------------------------------------------------------------------------------
def update_line(msg):
    global line
    line = msg


line_sub = rospy.Subscriber('line', Segment, update_line)
line = Segment()
# --------------------------------------------------------------------------------
# Publisher position
# --------------------------------------------------------------------------------
pose_pub = rospy.Publisher('car/pose', Pose2D, queue_size=1)

# --------------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------------
rate = rospy.Rate(10)
cmd = Twist()
# plt.ion()

while not rospy.is_shutdown():
    plt.clf()
    # Simulation
    car.simulate(cmd.linear.x, cmd.angular.z)
    # Affichage
    img = car.draw()
    plt.plot(img[0], img[1])
    plt.plot([line.entry.x, line.exit.x], [line.entry.y, line.exit.y])
    plt.axis([car.x - 50, car.x + 50, car.y - 50, car.y + 50])
    print 'Car position: {}, {}, {}'.format(car.x, car.y, car.theta)
    # Publication pose
    pose = Pose2D(x=car.x, y=car.y, theta=car.theta)
    pose_pub.publish(pose)
    plt.pause(rate.sleep_dur.to_sec())
    rate.sleep()
