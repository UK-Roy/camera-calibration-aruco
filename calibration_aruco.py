'''This script is for generating data
1. Provide desired path to store images.
2. Press 'c' to capture image and display it.
3. Press any button to continue.
4. Press 'q' to quit.
'''
import argparse
import cv2
import requests
import numpy as np
import os
from camera_calibration import calib
from take_imgs import take_images

# get the current working directory
current_working_directory = os.getcwd()

msg = f"To run this code you can pass two arguments: 1) The url of your camera(Mandatory), 2) Directory address where you will save your data (Optional: Otherwise it will save data in current directory) 3) Do you want to capture live image or you have directories(Optional: True or False), 4) Directory address where you will save your camera calibration matrix yaml file (Optional: Otherwise it will save data in current directory)"
# Initialize parser
parser = argparse.ArgumentParser(description = msg)
 
# Adding optional argument
parser.add_argument("-u", "--url", help = "Input url of your IP camera\n i.e. http://192.168.0.114:8080", required = True)
parser.add_argument("--online", help = "Do  you want to calibrate live or you have images folder for calibration", required = True, action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("-d", "--dir", help = "Directories where your camera images will be saved", required = False, default = current_working_directory)
parser.add_argument("-y", "--yaml", help = "Camera matrix yaml file directory", required = False, default = current_working_directory)

# Read arguments from command line
args = parser.parse_args()
url = args.url
path = f"{args.dir}/aruco_data"
yml_dir = args.yaml

if args.online:
    take_images(url=url, path=path)

calib(path=path, yml_dir=yml_dir)