#!/usr/bin/env python
import rospy
from regulation_imugps.msg import Segment
from geometry_msgs.msg import Point, Pose2D
from math import pi, cos


# --------------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------------

def deg2rad(deg):
    return deg * pi / 180


def ll2local(lat0, lon0, lat, lon):
    R = 6371000
    x = R * deg2rad(lat - lat0)
    y = R * cos(deg2rad(lat)) * deg2rad(lon - lon0)
    # x pointe vers le nord et y vers l'est et z vers le bas
    return [x, y]


# --------------------------------------------------------------------------------
# Node init
# --------------------------------------------------------------------------------
rospy.init_node('Navigation_line')

# --------------------------------------------------------------------------------
# List of Points to follow
# --------------------------------------------------------------------------------

pts = [Point(x=40, y=40),
       Point(x=40, y=-40),
       Point(x=-40, y=-40),
       Point(x=-40, y=40)]

segs = [Segment(entry=pts[i % len(pts)], exit=pts[(i + 1) % len(pts)])
        for i in range(len(pts))]
iseg = 0

# --------------------------------------------------------------------------------
# Current line to follow
# --------------------------------------------------------------------------------

cline = segs[iseg]
pub = rospy.Publisher('line', Segment, queue_size=1)


# --------------------------------------------------------------------------------
# Subscribe to pose to update the next line
# --------------------------------------------------------------------------------
def update_line(msg):
    global iseg, cline, pts
    if (msg.x - cline.exit.x) * (cline.entry.x - cline.exit.x) + (msg.y - cline.exit.y) * (cline.entry.y - cline.exit.y) < 0:
        print 'updated iseg'
        iseg = (iseg + 1) % len(pts)
        cline = segs[iseg]


sub = rospy.Subscriber('position', Pose2D, update_line)


# --------------------------------------------------------------------------------
# LOOP
# --------------------------------------------------------------------------------

rate = rospy.Rate(1)

while not rospy.is_shutdown():
    pub.publish(cline)
    print 'Current line:', iseg
    rate.sleep()
