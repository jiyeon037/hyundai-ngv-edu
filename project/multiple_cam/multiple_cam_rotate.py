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
    
    #영상 회전시키기 시작 ( 내장 카메라 )
    height_0, width_0, channel_0 = frame0.shape
    rotation_matrix = cv2.getRotationMatrix2D((width_0/2, height_0/2), 90, 1)
    frame0 = cv2.warpAffine(frame0, rotation_matrix, (width_0, height_0))
    #영상 회전시키기 끝


    #영상 회전시키기 시작 ( 웹캠 0 )
    height_1, width_1, channel_1 = frame1.shape
    rotation_matrix_1 = cv2.getRotationMatrix2D((width_1/2, height_1/2), 90, 1)
    frame1 = cv2.warpAffine(frame1, rotation_matrix_1, (width_1, height_1))
    #영상 회전시키기 끝

    #영상 회전시키기 시작 ( 웹캠 1 ) ## 90 부분을 조절하면 영상 회전 정도 조절가
    height_2, width_2, channel_2 = frame2.shape
    rotation_matrix_2 = cv2.getRotationMatrix2D((width_2/2, height_2/2), 90, 1)
    frame2 = cv2.warpAffine(frame2, rotation_matrix_2, (width_2, height_2))
    #영상 회전시키기 끝
    
    if(ret0):
        cv2.imshow("CAM0", frame0)

    if(ret1):
        cv2.imshow("CAM1", frame1)

    if(ret2):
        cv2.imshow("CAM2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료
    if cv2.waitKey(1) & 0xFF == ord('w'):
        print("CAPTURE")
        cv2.imwrite('capture1.png',frame1, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
        cv2.imwrite('capture2.png',frame2, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
        
video_capture_0.release()
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows() # 리소스 반환
