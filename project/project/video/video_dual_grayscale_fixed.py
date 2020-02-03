# 버그 수정된 버전 ( 외장 USB 사용 )

import numpy as np
import cv2

cv2.COLOR_RGB2GRAY
video_capture_1 = cv2.VideoCapture(1)

while True:

    ret1, frame1 = video_capture_1.read()
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
