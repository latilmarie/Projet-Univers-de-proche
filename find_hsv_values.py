import cv2
import numpy as np
import time

# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

# read first frame
cap0 = cv2.VideoCapture('C:/Users/azizb/Desktop/Cours/semestre2/projet/Nouveau dossier/videos/1_noir.mp4')
ret0, frame0 = cap0.read()


cap = cv2.VideoCapture('C:/Users/azizb/Desktop/Cours/semestre2/projet/Nouveau dossier/videos/1_noir.mp4')
cap.set(3,1280)
cap.set(4,720)
ret, frame = cap.read()
back_frame=frame0

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. 

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

 
while True:
    
    # Start reading the video feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        break
    #remove back_frame
    frame = 255-cv2.absdiff(frame, back_frame)
    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get the new values of the trackbar in real time as the user changes 
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    
    # Filter the image and get the binary mask, where white represents 
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)
 
    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Converting the binary mask to 3 channel image, this is just so 
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # stack the mask, orginal frame and the filtered result
    mask_3 = cv2.resize(mask_3,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    res = cv2.resize(res,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)


    stacked = np.hstack((mask_3,frame,res))
    
    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
    
    # If the user presses ESC then exit the program
    key = cv2.waitKey(100)
    if key == 27:
        break
    if key == 32:
            key2 = cv2.waitKey()
            if key2 == 27:
                break
            else:
                while key2 != 32:
                    pass
    
    # If the user presses `s` then print this array.
    if key == ord('s'):
        
        thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
        print(thearray)
        
        # Also save this array as penval.npy
        np.save('hsv_value',thearray)
        break
    
# Release the camera & destroy the windows.    
cap.release()
cv2.destroyAllWindows()