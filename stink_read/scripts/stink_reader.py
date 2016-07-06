#!/usr/bin/env python
import serial
import re
import rospy
from stink_read.msg import Rains


def bugs():
    pub = rospy.Publisher('bug_detect', Rains, queue_size=10)
    rospy.init_node('stink_bug_detector', anonymous=True)
    ser = serial.Serial("/dev/ttyACM0", 9600)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        serial_data=ser.readline()
        match = re.match(r'[0-9]+,([0-9].[0-9]+)+,1', serial_data,)
        msg = Rains()
        msg.header.stamp = rospy.Time.now()
        if match:
            msg.bug_seen = True
        else:
            msg.bug_seen = False
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        bugs()
    except rospy.ROSInterruptException:
        pass
