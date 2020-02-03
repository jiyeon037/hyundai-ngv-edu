#made by YONGYONG

import numpy as np
import cv2

cv2.COLOR_RGB2GRAY
#video_capture_0 = cv2.VideoCapture(0)
video_capture_1 = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    #ret0, frame0 = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()

    #if (ret0):
        # Display the resulting frame
        #cv2.imshow('Cam 0', frame0)
        #cv2.COLOR_RGB2GRAY
    if (ret1):
        # Display the resulting frame
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Cam 1', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture_0.release()
video_capture_1.release()
cv2.destroyAllWindows()
