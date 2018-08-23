#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

import numpy as np
import cv2
import socket
import sys
import StringIO


def sensors_callback(data, args):
    buff = StringIO.StringIO()
    data.serialize(buff)
    UDP_IP = IPAddress
    UDP_PORT = args[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    # sock.sendto(data.data,(UDP_IP,UDP_PORT))
    sock.sendto(buff.getvalue(), (UDP_IP, UDP_PORT))
    print('{} Sending Done.'.format(args[1]))

def rededge_callback(data):
    UDP_IP = IPAddress
    UDP_PORT = 5008
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(data.data, (UDP_IP, UDP_PORT))
    print('RedEdge Data sending done')


def send2Server():
    # if len(sys.argv)<2:
    #     print('You need to input IP Address!')
    #     sys.exit(1)
    
    rospy.init_node('listener',anonymous=True)
    try:
        global IPAddress 
        IPAddress = rospy.get_param("~server_ip")
    except KeyError:
        rospy.logerr('You need to input Server IP Address!Exit.')
        sys.exit(1)
    port_list = [5005,5006,5007]
    msg_list = ['Left Image','Right Image','Laser Scan']
    rospy.Subscriber('/stereo/left/image_raw/compressed',CompressedImage,sensors_callback,(port_list[0],msg_list[0]))
    rospy.Subscriber('/stereo/right/image_raw/compressed',CompressedImage,sensors_callback,(port_list[1],msg_list[1]))
    rospy.Subscriber('/scan',LaserScan,sensors_callback,(port_list[2],msg_list[2]))
    rospy.Subscriber('/rededge',String,rededge_callback)
    rospy.spin()

if __name__ == '__main__':
    send2Server()
