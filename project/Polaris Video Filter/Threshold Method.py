import os
import cv2
import numpy as np
import math
'''
1. 웹캠 이미지 리드
2. 그레이스케일로 변환
3. 픽셀 값의 평균으로 필터링: 평균값보다 크면 255(white), 작으면 0(black)
4. ROI 구역 설정 후 ROI 부분만 출력
'''
def im_trim(img, x, y, w, h):
    img = grayscale(img)

    (a, b) = img.shape[:2]
    center = (b/3 , a/1.5)
    angle90 = 90
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle90, scale)
    img = cv2.warpAffine(img, M, (a, b))
    '''
    x = 100; y = 100; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    '''
    img_trim = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다
    return img_trim


def grayscale(img): # 그레이스케일로 이미지 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def pixel_value_average(img): # 픽셀 값의 평균 계산
    sum = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            sum += img[i,j]
    pixel_N = img.shape[0] * img.shape[1]
    average = sum/pixel_N
    return average

def Filter(img, value = 0): # 픽셀 값 평균을 기준으로 필터링
    average = pixel_value_average(img)

    if value == 0:
        ret,img_filter = cv2.threshold(img, average, 255, cv2.THRESH_BINARY)
    else:
        ret,img_filter = cv2.threshold(img, average*value, 255, cv2.THRESH_BINARY)
       
    return img_filter

def count_pixel(img): # 픽셀 값이 0인 픽셀 COUNT
    number = cv2.countNonZero(img)

    return number

def pixel_ratio(img1, img2): # 픽셀 값 0 비율 계산
    if count_pixel(img1) == 0 | count_pixel(img2) ==0 :
        ratio = 0
    elif count_pixel(img1) < count_pixel(img2):
        ratio = count_pixel(img1)/count_pixel(img2)
    else:
        ratio = count_pixel(img2)/count_pixel(img1)
    return ratio

cap1 = cv2.VideoCapture(1) # 외장형 USB 웹캠1
cap2 = cv2.VideoCapture(0) # 외장형 USB 웹캠2

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()


    if (ret1 and ret2):

        frame1 = im_trim(frame1, 100, 100, 200, 200)
        frame2 = im_trim(frame2, 40, 200, 200, 200)

        '''
        x = 100; y = 100; #자르고 싶은 지점의 x좌표와 y좌표 지정
        w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    
        x = 70; y = 185; #자르고 싶은 지점의 x좌표와 y좌표 지정
        w = 200; h = 200; #x로부터 width, y로부터 height를 지정
        '''
        thresh1 = Filter(frame1)
        thresh2 = Filter(frame2)

        print(pixel_ratio(thresh1, thresh2))

        cv2.imshow("1", thresh1)
        cv2.imshow("2", thresh2)
        cv2.imshow("ORIGIN", frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료
    
cap1.release()
cap2.release()
cv2.destroyAllWindows() # 리소스 반환
cv2.waitKey(0)