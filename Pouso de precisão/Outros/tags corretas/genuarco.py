import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import cv2.aruco as aruco






# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, 10, 2000)
cv2.imwrite("10.jpg", img)

# Display the image to us
cv2.imshow('frame', img)
# Exit on any key
cv2.waitKey(0)









# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, 4, 2000)
cv2.imwrite("4.jpg", img)

# Display the image to us
cv2.imshow('frame', img)
# Exit on any key
cv2.waitKey(0)








# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, 15, 2000)
cv2.imwrite("15.jpg", img)

# Display the image to us
cv2.imshow('frame', img)
# Exit on any key
cv2.waitKey(0)








# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, 20, 2000)
cv2.imwrite("20.jpg", img)

# Display the image to us
cv2.imshow('frame', img)
# Exit on any key
cv2.waitKey(0)








# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, 25, 2000)
cv2.imwrite("25.jpg", img)

# Display the image to us
cv2.imshow('frame', img)
# Exit on any key








cv2.waitKey(0)
cv2.destroyAllWindows()
