#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Joy, NavSatFix
from geometry_msgs.msg import Point


def joy_callback(msg):
    if msg.buttons[12] == 1:
        gps_goal = NavSatFix()
        gps_goal.latitude = 33.726526
        gps_goal.longitude = -83.299984
        gps_put.publish(gps_goal)
    if msg.buttons[14] == 1:
        client.cancel_all_goals()


def point_callback(msg):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'utm'
    goal.target_pose.pose.position.x = msg.x
    goal.target_pose.pose.position.y = msg.y
    goal.target_pose.pose.position.z = msg.z
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    client.cancel_all_goals()
    client.send_goal(goal)


if __name__ == '__main__':
    rospy.init_node('gps_nav')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    joy_sub = rospy.Subscriber('bluetooth_teleop/joy', Joy, joy_callback)
    gps_put = rospy.Publisher('gps_nav/gps', NavSatFix, queue_size=10)
    gps_get = rospy.Subscriber('gps_nav/utm', Point, point_callback)

    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        rate.sleep()
