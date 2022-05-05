# import the necessary packages
from collections import deque
import cv2
import imutils
import time
import matplotlib.pyplot as plt

ESC_KEY = 27     #Touche Echap
PAUSE_KEY = 32   #Touche espace
INTERVAL= 100     #intervalle
FRAME_RATE = 30  #fp

Lower_green = (0, 15, 0)
Upper_green = (255, 255, 255) 

Lower_blue = (103, 29, 0)
Upper_blue = (255, 255, 255) 

# get back_frame
cap0 = cv2.VideoCapture('2_billes_3kg_noir.mp4')
ret0, frame0 = cap0.read()

# queue to put the coordinates of the ball
pts = deque()
pts1 = deque()

cap = cv2.VideoCapture('2_billes_3kg_noir.mp4')

    
# allow the video file to warm up
time.sleep(2.0)
ret, frame = cap.read()
back_frame = frame0
shape = back_frame.shape
k=0
# keep looping
while True:

    ret, frame = cap.read()
    k=k+1
    if not ret:
        break
    if k > 170 :
        
        frame1=frame
        #remove back_frame
        frame = 255-cv2.absdiff(frame, back_frame)
        # blur it, and convert it to the HSV
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
    	# construct a mask for the color, then perform dilationstons
        mask2 = cv2.inRange(hsv, Lower_blue, Upper_blue)
        mask1 = cv2.inRange(hsv, Lower_green, Upper_green)
    # 	mask = cv2.erode(mask, None, iterations=2)
        mask2 = cv2.dilate(mask2, None, iterations=5)   
        
        
    # 	mask = cv2.erode(mask, None, iterations=2)
        mask1 = cv2.dilate(mask1, None, iterations=5)
        
   
        #Ball 1 :
     	# find contours in the mask and initialize the current
     	# (x, y) center of the ball
        cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
     	# only proceed if at least one contour was found
        if len(cnts) > 0:
    		
            c=max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    		# only proceed if the radius meets a minimum size
            if radius > 5 :
                cv2.circle(frame1, center, 5, (0, 255, 0), -1)
                pts.appendleft(center)
     	
 
        #Ball 2 :        
        cnts1 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1)
        center1 = None
     	# only proceed if at least one contour was found
        if len(cnts1) > 0:
    
            c1=max(cnts1, key=cv2.contourArea)
            ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
    		# only proceed if the radius meets a minimum size
            if radius1 > 5 :
                cv2.circle(frame1, center1, 5, (255, 0, 0), -1)
                pts1.appendleft(center1)

        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(10)
        if key == ESC_KEY:
            break
        if key == PAUSE_KEY:
            key2 = cv2.waitKey()
            if key2 == ESC_KEY:
                break
            else:
                while key2 != PAUSE_KEY:
                    pass

cap.release()
# close all windows
cv2.destroyAllWindows()

# show tracjectories of the two balls 
liste1 = []
liste2 = []
for i in range(len(pts)):
    if pts[i]!= None :
        liste1.append(pts[i][0])
        liste2.append(shape[1] - pts[i][1])
plt.plot(liste1[:],liste2[:],'g')

liste_a = []
liste_b = []
for i in range(len(pts1)):
    if pts1[i]!= None :
        liste_a.append(pts1[i][0])
        liste_b.append(shape[1] - pts1[i][1])
plt.plot(liste_a[:],liste_b[:],'b')
