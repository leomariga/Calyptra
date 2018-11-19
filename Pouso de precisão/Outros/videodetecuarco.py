import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import cv2.aruco as aruco
import math





# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
 
 
# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :
 
    assert(isRotationMatrix(R))
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])


 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        img = frame.array


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
                rvec = np.zeros((ids.shape[0], 3))
                tvec = np.zeros((ids.shape[0], 3))
     
                gray = aruco.drawDetectedMarkers(gray, corners, borderColor=(0, 255, 0))
                cameraMatrix = np.array([[631.43076033,   0,         319.46293155],[  0,         630.14567027, 241.75853213],[  0,           0,           1,        ]])
                distCoeffs =  np.array([[ 0.06375513, -0.05092762,  0.00133275, -0.00200469, -0.56225284]])
                #print(cameraMatrix)

                
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.1, cameraMatrix, distCoeffs, rvec, tvec)
                #print(rvec)
                #print(tvec)
                ids = ids.reshape(1,-1)
                #print(ids)
                somaSin = [0, 0, 0]
                somaCos = [0, 0 ,0]
                somaPos = [0 ,0, 0]
                for i in range(ids.shape[1]):
                        #print("foi",i)
                        aruco.drawAxis(gray, cameraMatrix, distCoeffs, rvec[i], tvec[i], 0.1);
                        aruco
                        rmat = cv2.Rodrigues(rvec[i])[0]
                        yawpitchroll_radian = -rotationMatrixToEulerAngles(rmat)
                        yawpitchroll_radian[0] = yawpitchroll_radian[0]-math.pi
                        yawpitchroll_angles = 180*yawpitchroll_radian/math.pi
                        #print(corners[i][0][0])
                        somaSin = somaSin + np.sin(yawpitchroll_radian)
                        somaCos = somaCos + np.cos(yawpitchroll_radian)
                        somaPos = somaPos + tvec[i, 0]
                        cv2.putText(gray,'Id: '+str(ids[0,i]),(int(corners[i][0][0][0]),int(corners[i][0][0][1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),2,cv2.LINE_AA)


                mediaSin = somaSin/ids.shape[1]
                mediaCos = somaCos/ids.shape[1]
                mediaAngulos = 180*np.arctan2(mediaSin, mediaCos)/math.pi
                mediaPos = somaPos/ids.shape[1]

                #print(mediaAngulos)
                #print(mediaPos)
                
                cv2.putText(gray,'Aerodream Precision Landing System',(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Deslocamento:',(10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'X: '+str(round(mediaPos[0]*100,2))+' cm',(10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Y: '+str(round(mediaPos[1]*100,2))+' cm',(10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Z: '+str(round(mediaPos[2]*100-3,2))+' cm',(10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Angulo:',(10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Pitch: '+str(round(mediaAngulos[0],2))+' graus',(10,140), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Roll: '+str(round(mediaAngulos[1],2))+' graus',(10,160), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(gray,'Yaw: '+str(round(mediaAngulos[2],2))+' graus',(10,180), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2,cv2.LINE_AA)
        
     
                #print(rejectedImgPoints)
                # Display the resulting frame
        cv2.imshow('frame',gray)
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if (key == ord("q")):
                break
	
cv2.imwrite("ttceufie.png",image)
