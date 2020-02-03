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
def resize(img, ratio, dsize=None, dst=None):
    return cv2.resize(img, dsize, dst, ratio, ratio, interpolation=cv2.INTER_AREA)

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
        ret,img_filter = cv2.threshold(img, average *0.7, 255, cv2.THRESH_BINARY)
    else:
        ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
       
    return img_filter

def count_pixel(img): # 픽셀 값이 0인 픽셀 COUNT
    number = cv2.countNonZero(img)
    return number

## 이 부분이 수정됨.

def pixel_ratio(img1, img2): # 픽셀 값 0 비율 계산
    temp1 = count_pixel(img1)
    temp2 = count_pixel(img2)
    if temp1 >0 and temp2> 0:

        if temp1 < temp2:
            ratio = temp1/temp2
            return ratio
        else:
            ratio = temp2/temp1
            return ratio
    return 99
def vertices_multicam(img, distance, width, direction, angle = 54): 
    '''
    관심 영역 설정 - 거리에 따른 roi 설정
    height = img.shape[0]
    width = img.shape[1]
    distance = 카메라와 측정 대상까지의 거리
    width = 카메라 간격
    !!! distance와 width의 단위는 같아야한다. !!!
    direction = 카메라 위치(0: Right, 1: Left)
    angle = 카메라 화각
    '''
    imshape = img.shape 
    angle = angle * (math.pi/180)
    F = int(width / (2*distance*math.tan(angle)))

    if direction: # Left = 1
        lower_left = [imshape[1]*F, imshape[0]]
        lower_right = [imshape[1], imshape[0]]
        higher_left = [imshape[1]*F, 0]
        higher_right = [imshape[1], 0]
    else: # Right = 0
        lower_left = [0,imshape[0]]
        lower_right = [imshape[1]*(1 - F), imshape[0]]
        higher_left = [0, 0]
        higher_right = [imshape[1]*(1 - F), 0]
    
    vertices = [np.array([lower_left, lower_right, higher_right, higher_left], dtype = np.int32)]
    return vertices

def vertices_road(img): # 관심 영역 설정 - 사다리꼴(도로 부분 할당)
    imshape = img.shape 
        
    lower_left = [0, imshape[0]]
    lower_right = [imshape[1], imshape[0]]
    higher_left = [imshape[1]/2-imshape[1]/8, 5*imshape[0]/8]
    higher_right = [imshape[1]/2+imshape[1]/8, 5*imshape[0]/8]
 
    vertices = [np.array([lower_left, lower_right, higher_right, higher_left], dtype = np.int32)]
    return vertices

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅
 
    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지
    
    if len(img.shape) > 2: # Color 이미지(3채널)라면 :
        color = color3
    else: # 흑백 이미지(1채널)라면 :
        color = color1
        
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 
    cv2.fillPoly(mask, vertices, color)
    
    # 이미지와 color로 채워진 ROI를 합침
    roi_image = cv2.bitwise_and(img, mask)
    return roi_image

def show_convert_video(frame, CAM, direction): # frame과 window창 이름 설정
    vertice_set = vertices_multicam(frame, 20, 3, direction)
    #vertice_set = vertices_road(frame)
    frame = grayscale(frame)
    frame = Filter(frame)
    frame = region_of_interest(frame, vertice_set)
    '''
    h, w = frame.shape[:2]
    M1 = cv2.getRotationMatrix2D((h / 2, w / 2), 90, 1) 
    frame = cv2.warpAffine(frame, M1, (h, w)) 
    '''
    cv2.imshow( CAM , frame)
    return frame

video_capture_1 = cv2.VideoCapture(1) # 외장형 USB 웹캠1
video_capture_2 = cv2.VideoCapture(2) # 외장형 USB 웹캠2

ret1, frame1 = video_capture_1.read()
ret2, frame2 = video_capture_2.read()

while True:
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()

    #ret2, frame2 = video_capture_2.read()

    if (ret1 and ret2):

        img1= show_convert_video(frame1, "CAM0", 0)
        img2= show_convert_video(frame2, "CAM1", 1)
        #print(pixel_ratio(frame0, frame1))
        A = pixel_ratio(img1, img2) # 대입인자는 이미 0 또는 1만 있는 이미지만 대입
        print(A)       
    
    #if(ret2):
        #show_convert_video(frame2, "CAM2")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료

video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows() # 리소스 반환
