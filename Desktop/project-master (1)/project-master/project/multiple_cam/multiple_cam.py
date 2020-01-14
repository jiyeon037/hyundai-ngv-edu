# 노트북 내장 웹캠 및 USB 웹캠 사용할 수 있도록 하는 파이썬 코드
# 다중 웹캠 지원 
import numpy as np
import cv2

video_capture_0 = cv2.VideoCapture(0) #노트북 내장 웹캠
video_capture_1 = cv2.VideoCapture(1) # 외장형 USB 웹캠1
video_capture_2 = cv2.VideoCapture(2) # 외장형 USB 웹캠2

while True:
    ret0, frame0 = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()
    if(ret0):
        cv2.imshow("CAM0", frame0)

    if(ret1):
        cv2.imshow("CAM1", frame1)

    if(ret2):
        cv2.imshow("CAM2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료
    
video_capture_0.release()
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows() # 리소스 반환
