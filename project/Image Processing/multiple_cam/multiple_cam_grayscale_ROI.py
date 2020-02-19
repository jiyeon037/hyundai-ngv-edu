# 노트북 내장 웹캠 및 USB 웹캠 사용할 수 있도록 하는 파이썬 코드
# 다중 웹캠 지원 
import numpy as np
import cv2

def grayscale(img): # 흑백 이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 
def hsvscale(img): # HSV 이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
 
def canny(img, low_threshold, high_threshold): # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)
 
def gaussian_blur(img, kernel_size): # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
 
def vertices(img): # 관심 영역 설정
    imshape = img.shape 
        
    lower_left = [0, imshape[0]]
    lower_right = [imshape[1], imshape[0]]
    higher_left = [imshape[1]/2-imshape[1]/8, 5*imshape[0]/8]
    higher_right = [imshape[1]/2+imshape[1]/8, 5*imshape[0]/8]
 
    vertices = [np.array([lower_left, lower_right, higher_right, higher_left], dtype = np.int32)]
    return vertices
 
def yellowRange(hsv_img): # hsv_img 노란색 검출 
    lower_yellow = np.array([20, 100, 100], dtype='uint8')
    higher_yellow = np.array([100, 255, 255], dtype='uint8')
    mask_yellow = cv2.inRange(hsv_img, lower_yellow, higher_yellow)
    return mask_yellow
 
def whiteRange(gray_img): # gray_img 흰색 검출
    mask_white = cv2.inRange(gray_img, 200, 255) # 색을 통한 추출
    return mask_white

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
        gray_img = grayscale(frame1) # 흑백 이미지로 변환
        hsv_img = hsvscale(frame1) # hsv 이미지로 변환        
        
        mask_yellow = yellowRange(hsv_img) # 노란색 검출
        mask_white = whiteRange(gray_img) # 흰색 검출
        
        mask_add = cv2.bitwise_or(mask_white, mask_yellow) 
        mask_img = cv2.bitwise_and(gray_img, mask_add)
        blur_img = gaussian_blur(mask_img, 3) # Blur 효과
        canny_img = canny(blur_img, 50, 150) # Canny edge 알고리즘
        vertice_set = vertices(canny_img) # 관심영역 설정

        frame1 = region_of_interest(gray_img, vertice_set)     
        cv2.imshow("CAM1", frame1)

    if(ret2):
        gray_img = grayscale(frame2) # 흑백 이미지로 변환
        hsv_img = hsvscale(frame2) # hsv 이미지로 변환        
        
        mask_yellow = yellowRange(hsv_img) # 노란색 검출
        mask_white = whiteRange(gray_img) # 흰색 검출
        
        mask_add = cv2.bitwise_or(mask_white, mask_yellow) 
        mask_img = cv2.bitwise_and(gray_img, mask_add)
        blur_img = gaussian_blur(mask_img, 3) # Blur 효과
        canny_img = canny(blur_img, 50, 150) # Canny edge 알고리즘
        vertice_set = vertices(canny_img) # 관심영역 설정

        frame2 = region_of_interest(gray_img, vertice_set)     
        cv2.imshow("CAM2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료
    
video_capture_0.release()
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows() # 리소스 반환
