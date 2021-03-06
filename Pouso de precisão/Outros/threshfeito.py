import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
import cv2

import numpy as np
from matplotlib import pyplot as plt


##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
MORPH2 = 5
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

img = cv2.imread('tag3.png')

gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

gray = cv2.bilateralFilter( gray, 1, 10, 120 )

edges  = cv2.Canny( gray, 10, CANNY )

kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

kernel2 = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH2, MORPH2) )

closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

#dilation = cv2.dilate(closed,kernel)

#opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel2)

__,contours, h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

for cont in contours:


	if cv2.contourArea( cont ) > 5000 :

		arc_len = cv2.arcLength( cont, True )

		approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )

		if ( len( approx ) >= 4 ):
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
cv2.imshow( 'edges', closed )

cv2.namedWindow( 'rgb')
cv2.imshow( 'rgb', img )




#cv.drawContours( img, squares, -1, (0, 255, 0), 3 )
#cv.imshow('squares', img)
#res = np.hstack((img, th, edged))
##cv.imshow("Game Boy Screen", res)
cv2.waitKey(0)

