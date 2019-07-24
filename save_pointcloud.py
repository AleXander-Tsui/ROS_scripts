#!/usr/bin/env python
import rospy
import cv2
import cv_bridge
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
import sensor_msgs.point_cloud2 as pc2

import sys, select, termios, tty

def save_image(num):
    image = rospy.wait_for_message(
            "/camera/rgb/image_raw",
            Image)
    # Decode to cv2 image and store
    img_file_path = "/home/tsui/Data/GMM/" + str(num) + ".jpg"
    cv2.imwrite(img_file_path, cv_bridge.CvBridge().imgmsg_to_cv2(image))

def save_pose(num):
    odom = rospy.wait_for_message(
            "/odom",
            Odometry)
    # Decode to cv2 image and store
    img_file_path = "/home/tsui/Data/GMM/" + str(num) + "_pose.txt"
    with open(img_file_path, "w") as file:
        file.write(str(odom.pose.pose.position.x)+" "+str(odom.pose.pose.position.y)+" "+str(odom.pose.pose.position.z)+" "+str(odom.pose.pose.orientation.x)+" "+
                   str(odom.pose.pose.orientation.y)+" "+str(odom.pose.pose.orientation.z)+" "+str(odom.pose.pose.orientation.w))

def save_pointcloud(num):
    points = rospy.wait_for_message("/ORB_SLAM2_SP/PointCloud", PointCloud2)
    img_file_path = "/home/tsui/Data/GMM/" + str(num) + "_pointcloud.txt"
    with open(img_file_path, "w") as file:
        for p in pc2.read_points(points, field_names = ("x", "y", "z"), skip_nans=True):
            file.write(str(p[0])+" "+str(p[1])+" "+str(p[2])+" "+"\n")

rospy.init_node('save_points')
num = 0
while(1):
    num = num + 1
    save_pointcloud(num)
    save_image(num)
    save_pose(num)

