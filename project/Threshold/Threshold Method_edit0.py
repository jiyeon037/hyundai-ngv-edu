import os
import cv2
import numpy as np
import math
import sys

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
        #ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
       
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
    return ratio*100

def pixel_ratio0(img1, img2): # 픽셀 값 0 비율 계산
    ratio = (count_pixel(img2)-count_pixel(img1))/img1.size
    return ratio*100

def nothing(x):
    pass #더미 함수 생성... 트랙 바 생성시 필요하므로

def same_bright(frame, gap):
    if gap>=0:
        M = np.ones(frame.shape, dtype = "uint8") * abs(int(gap))
        transform = cv2.add(frame, M)
    else:
        M = np.ones(frame.shape, dtype = "uint8") * abs(int(gap))
        transform = cv2.subtract(frame, M)
    
    return transform

def seperated_image_ratio(frame1, frame2, unit):
    ratio_arr = np.zeros((unit,unit), dtype = int)
    U = int(frame1.shape[0]/unit)

    #격자 그리기
    for x in range(unit): cv2.line(frame1, (U*x, 0), (U*x, U*unit), (0,0,0), 1, 4)
    for y in range(unit): cv2.line(frame1, (0, U*y), (U*unit, U*y), (0,0,0), 1, 4)

    #ratio 행렬 생성
    for i in range(unit):
        for j in range(unit):
            img_trim1 = frame1[i*U:(i+1)*U, j*U:(j+1)*U]
            img_trim2 = frame2[i*U:(i+1)*U, j*U:(j+1)*U]
            ratio = int(pixel_ratio(img_trim1, img_trim2))
            ratio_arr[i,j] = ratio

            text = '('+str(i)+','+str(j)+')'
            cv2.putText(frame1, text, (j*U+int(U*0.2), i*U+int(U*0.4)), 1, 0.8, (0, 0, 0))
            cv2.putText(frame1, str(ratio), (j*U+int(U*0.3), i*U+int(U*0.7)), 1, 1, (0, 0, 0))
            #cv2.line(frame1, (int(U*(i+0.5)), int(U*(j+0.5))), (int(U*(i+0.5)), int(U*(j+0.5))), (0,0,0), 5)
           
    return ratio_arr           

cap1 = cv2.VideoCapture(0) # 외장형 USB 웹캠1 (위쪽이 0번)-R
cap2 = cv2.VideoCapture(1) # 외장형 USB 웹캠2 (아래쪽이 1번)-L

cv2.namedWindow('Binary') #트랙바를 붙일 윈도우를 생성
cv2.createTrackbar('threshold','Binary', 0, 150, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('threshold', 'Binary', 100) #초기값 100
cv2.createTrackbar('X','Binary', 0, 100, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('X', 'Binary', 40) #초기값 40
cv2.createTrackbar('Y','Binary', 150, 250, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('Y', 'Binary', 200) #초기값 200

#sys.stdout = open('output.txt','w') #print 값 output.txt파일로 저장

count = 0

while True:
    ret1, f1 = cap1.read()
    ret2, f2 = cap2.read()

    TH = cv2.getTrackbarPos('threshold','Binary')*0.01 # threshold 필터링 값
    x = cv2.getTrackbarPos('X','Binary') # frame2의 x축 값 변경
    y = cv2.getTrackbarPos('Y','Binary') # frame2의 y축 값 변경

    if (ret1 and ret2):

        frame1 = im_trim(f1, 72, 100, 300, 300)
        frame2 = im_trim(f2, x, y, 300, 300) # x 초기값 40, y 초기값 200

        average1 = pixel_value_average(frame1)
        average2 = pixel_value_average(frame2)
        gap = average1 - average2

        frame2_c = same_bright(frame2, gap)
            
        average2_c = pixel_value_average(frame2_c)

        thresh1 = Filter(frame1, TH)
        thresh2 = Filter(frame2_c, TH)

        thresh3 = cv2.bitwise_xor(thresh1, thresh2) # t1, t2 이미지 겹치는 부분 0으로 변환
        
        ratio_arr = seperated_image_ratio(thresh1, thresh2, 6)  #pixel이 300*300 이므로 unit은 300의 약수여야함
        

        N=0
        for i in range(6):
            for j in range(6):
                if sep_ratio_arr[i,j]>94: 
                    sep_ratio_arr[i,j]=0
                else: 
                    N+=1
        p_ratio = int(sep_ratio_arr.sum()/N)
    
        xor_ratio = count_pixel(thresh3) * 100/ thresh3.size
    
        #p_ratio = int(pixel_ratio(thresh1, thresh2)) # t1, t2의 검은색 픽셀 수 비율 계산
        
     
        if (p_ratio<85 and p_ratio>0):
            count += 1
        else:
            count = 0

        if count > 6:
            print('',\
            'R: '+ str(p_ratio),\
            'TH: ' + str(TH),\
            'GAP: ' + str(int(gap)),\
            'A1: ' + str(int(average1)),\
            'XOR: ' + str(int(xor_ratio)),\
            'COUNT: ' + str(count),\
            'WET ROAD DETECTED!!!',\
            '',\
            sep = ' | ')

            count = 0

        else:
            print('',\
            'R: '+ str(p_ratio),\
            'TH: ' + str(TH),\
            'GAP: ' + str(int(gap)),\
            'A1: ' + str(int(average1)),\
            'XOR: ' + str(int(xor_ratio)),\
            'COUNT: ' + str(count),\
            '',\
            sep = ' | ')

        cv2.imshow("1", thresh1)
        cv2.imshow("2", thresh2)
        cv2.imshow("3", thresh3)
        cv2.imshow("ORIGIN1", frame1)
        #cv2.imshow("ORIGIN2", frame2_c)
        #cv2.imshow("O", f1)
        #cv2.imshow("O,", f2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료

cap1.release()
cap2.release()
cv2.destroyAllWindows() # 리소스 반환
cv2.waitKey(0)