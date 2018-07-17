#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan

import numpy as np
import cv2
import socket
import sys
import StringIO

def left_callback(data):
    UDP_IP = sys.argv[1]
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(data.data, (UDP_IP, UDP_PORT))
    #np_arr = np.fromstring(data.data, np.uint8)
    #image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #cv2.imwrite('/home/asctec/Desktop/left_image.jpg',image_np)
    print('Left Image sending done')
def right_callback(data):
    UDP_IP = sys.argv[1]
    UDP_PORT = 5006
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(data.data, (UDP_IP, UDP_PORT))
    #np_arr = np.fromstring(data.data, np.uint8)
    #image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #cv2.imwrite('/home/asctec/Desktop/right_image.jpg',image_np)
    print('Right Image sending done')
def laser_callback(data):
    laser_buff = StringIO.StringIO()
    data.serialize(laser_buff)
    UDP_IP = sys.argv[1]
    UDP_PORT = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(laser_buff.getvalue(), (UDP_IP, UDP_PORT))
    print('Laser Data sending done')

def send2Server():
    if len(sys.argv)<2:
        print('You need to input IP Address!')
        sys.exit(1)
    rospy.init_node('listener',anonymous=True)
    rospy.Subscriber('/stereo/left/image_raw/compressed',CompressedImage,left_callback)
    rospy.Subscriber('/stereo/right/image_raw/compressed',CompressedImage,right_callback)
    rospy.Subscriber('/scan',LaserScan,laser_callback)
    rospy.spin()

if __name__ == '__main__':
    send2Server()
