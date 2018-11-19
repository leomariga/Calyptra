import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
# 420x600 oranı 105mmx150mm gerçek boyuttaki kağıt için
_width  = 600.0
_height = 420.0
_margin = 0.0
##################


corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 )

 
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

        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

        gray = cv2.bilateralFilter( gray, 1, 10, 120 )

        edges  = cv2.Canny( gray, 10, CANNY )

        kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

        closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

        __,contours, h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

        for cont in contours:

                # Küçük alanları pass geç
                if cv2.contourArea( cont ) > 500 :

                        arc_len = cv2.arcLength( cont, True )

                        approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )

                        if ( len( approx ) == 4 ):
                                IS_FOUND = 1
                                #M = cv2.moments( cont )
                                #cX = int(M["m10"] / M["m00"])
                                #cY = int(M["m01"] / M["m00"])
                                #cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

                                pts_src = np.array( approx, np.float32 )

                                h, status = cv2.findHomography( pts_src, pts_dst )
                                out = cv2.warpPerspective( img, h, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) )

                                cv2.drawContours( img, [approx], -1, ( 255, 0, 0 ), 2 )

                        else : pass

        #cv2.imshow( 'closed', closed )
        #cv2.imshow( 'gray', gray )
        cv2.namedWindow( 'edges')
        cv2.imshow( 'edges', edges )

        cv2.namedWindow( 'rgb')
        cv2.imshow( 'rgb', img )
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if (key == ord("q")):
                break
	
cv2.imwrite("ttceufie.png",image)
