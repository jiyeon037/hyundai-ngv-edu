# MADE BY jiyeon + YOONSEOCK (feat yong taeck)
# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np

def grayscale(img): # 흑백 이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 

video_caputre_1 = cv2.VideoCapture(0) # 외장형 USB 웹캠1
video_caputre_2 = cv2.VideoCapture(1) # 외장형 USB 웹캠2

while True:
    ret1, frame1 = video_caputre_1.read()
    ret2, frame2 = video_caputre_2.read()


   #if(ret1):
    #    gray_img = grayscale(frame1) # 흑백 이미지로 변환
     #   grayA = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
      #  cv2.imshow("CAM1", frame1)

        
  #  if(ret2):
      #  gray_img = grayscale(frame2) # 흑백 이미지로 변환
     #  grayB = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
      #  cv2.imshow("CAM2", frame2)


    if(ret1 and ret2):
        
        grayA = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        cv2.imshow("CAM1", grayA)
        cv2.imshow("CAM2", grayB)
        
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        cv2.imshow("Thresh", thresh)

        print("SSIM: {}".format(score))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 OpenCV 종료

video_caputre_1.release()
video_caputre_2.release()

cv2.destroyAllWindows() # 리소스 반환

cv2.waitKey(0)
