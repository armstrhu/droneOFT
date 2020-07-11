

import sys
import cv2
import numpy as np
 
 # Mouse function
def select_point(event, x, y, flags, params):
    global point, point_selected, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)
 
# Lucas kanade params
lk_params = dict(winSize = (15, 15), maxLevel = 3,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.01))
 
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)
 
point_selected = False
point = ()
old_points = np.array([[]])

#cap = cv2.VideoCapture(0) # webcam
cap = cv2.VideoCapture(sys.argv[1]) # video file
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
 
# Create old frame
_, frame = cap.read()
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

feature_params = dict( maxCorners = 2,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
old_points = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)[1]
point = (old_points[0][0], old_points[0][1])
print point
point_selected = True

cv2.imshow("Frame", frame)

print "video will pause for 5 seconds.  Use mouse to seed initial guess for drone tracker."
cv2.waitKey(5000)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if point_selected is True:
            cv2.circle(frame, point, 5, (0, 255, 0), 2)
     
            new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
            old_gray = gray_frame.copy()
            old_points = new_points
     
            x, y = new_points.ravel()
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
     
        cv2.imshow("Frame", frame)
    else:
        break
 
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()