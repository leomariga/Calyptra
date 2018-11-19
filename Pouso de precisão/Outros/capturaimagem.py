import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
import cv2

from picamera.array import PiRGBArray
from picamera import  PiCamera
import time

camera = PiCamera()

rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imshow("Image", image)
time.sleep(3)
cv2.imwrite('ttceufie.png',image)
cv2.waitKey(0)
