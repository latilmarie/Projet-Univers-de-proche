# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import matplotlib.pyplot as plt


# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()
liste1 = [[],[]]
liste2 = [[],[]]


vs = cv2.VideoCapture('2_billes_3kg_noir.mp4')

frameTime = 100
shape=(460,600)
# loop over frames from the video stream
while True:
	# grab the current frame, 
	ret,frame = vs.read()
	# check to see if we have reached the end of the stream
	if not ret :
		break

	# resize the frame (so we can process it faster)
	frame = imutils.resize(frame, width=shape[0],height=shape[1])
    
	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked
	(success, boxes) = trackers.update(frame)
	# loop over the bounding boxes and draw then on the frame
	for i in range(len(boxes)):
		(x, y, w, h) = [int(v) for v in boxes[i]]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		liste1[i].append(x+w/2)
		liste2[i].append(shape[1]-y+h/2)
        
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(frameTime) & 0xFF
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		# create a new object tracker for the bounding box and add it
		# to our multi-object tracker
		tracker = OPENCV_OBJECT_TRACKERS["csrt"]()
		trackers.add(tracker, frame, box)
        
	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break
vs.release()
plt.figure()
plt.axes().set_aspect('equal')
plt.plot(liste1[0][:],liste2[0][:],'r')
plt.plot(liste1[1][:],liste2[1][:],'b')
plt.show()
# close all windows
cv2.destroyAllWindows()

