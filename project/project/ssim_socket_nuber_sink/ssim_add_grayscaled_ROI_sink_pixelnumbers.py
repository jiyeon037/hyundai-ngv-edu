
# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np
import socket
'''

def doCanny(input, lowThresh, highThresh, aperture):
    if input.nChannels != 1:
            return(0)
    out = cv.CreateImage((input.width, input.height), input.depth, 1)
    cv.Canny(input, out, lowThresh, highThresh, aperture)
    return out

def doPyrDown(input):
    assert(input.width !=0 and input.height !=0)
    out = cv.CreateImage((input.width/2, input.height/2), input.depth, input.nChannels)
    cv.PyrDown(input, out)
    return out

'''
def im_trim1(img): #함수로 만든다
    x = 100; y = 100; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    img_trim1 = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다
    #cv2.imwrite('org_trim.jpg',img_trim) #org_trim.jpg 라는 이름으로 저장
    return img_trim1 #필요에 따라 결과물을 리턴

def im_trim2(img): #함수로 만든다
    x = 70; y = 185; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    img_trim2 = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다
    #cv2.imwrite('org_trim.jpg',img_trim) #org_trim.jpg 라는 이름으로 저장
    return img_trim2 #필요에 따라 결과물을 리턴



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
        
        (h, w) = frame1.shape[:2]
        (h, w) = frame2.shape[:2]
        
        center = (w/3 , h/1.5)
 
        angle90 = 90
        angle180 = 180
        angle270 = 270
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle90, scale)
        rotated901 = cv2.warpAffine(frame1, M, (h, w))
        M = cv2.getRotationMatrix2D(center, angle90, scale)
        rotated902 = cv2.warpAffine(frame2, M, (h, w))
        
        grayA = cv2.cvtColor(rotated901, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(rotated902, cv2.COLOR_BGR2GRAY)


        asd= im_trim1(grayA)#trim_image 변수에 결과물을 넣는다
        qwe= im_trim2(grayB)

        cv2.imshow("CAM1", asd)
        cv2.imshow("CAM2", qwe)
        
        (score, diff) = compare_ssim(asd, qwe, full=True)
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        cv2.imshow("Thresh", thresh)


#        pimg3 = doCanny(thresh, 10, 100, 3)
#        pimg2 = doPyrDown(pimag2)
#        cv2.imshow("Example 2", pimg2)

        print("SSIM: {}".format(score))
        nzCount = cv2.countNonZero(thresh)
        print("numbers {}".format(nzCount))
        
        key = cv2.waitKey(1)

        


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 OpenCV 종료

video_caputre_1.release()
video_caputre_2.release()

cv2.destroyAllWindows() # 리소스 반환

cv2.waitKey(0)
