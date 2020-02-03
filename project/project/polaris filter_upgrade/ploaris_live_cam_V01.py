
import os
import cv2
import numpy as np

# 카메라를 통해 사진을 촬영해서 폴더에 이미지를 저장하는 부분
# 파일의 저장 및 읽기 프로세스가 많아서 속도가 느려지는 요인이 되는 것으로 추정
# 추후 프로젝트 소스코드 합칠 때는 파일의 읽기/쓰기 최소화 필요
# 본 파이썬 코드와 동일 위치에 image seed 라는 이름의 빈 폴더 필요함.

def capture_video_to_img():
    video_capture_1 = cv2.VideoCapture(1)
    video_capture_2 = cv2.VideoCapture(2)
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()
    directoryname = os.path.dirname(os.path.realpath(__file__))
    cv2.imwrite(directoryname + '/image seed/'+'capture1.png',frame1, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cv2.imwrite(directoryname + '/image seed/'+'capture2.png',frame2, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    video_capture_1.release()
    video_capture_2.release()
    
def resize(img, ratio, dsize=None, dst=None):
    resizeimg = cv2.resize(img, dsize, dst, ratio, ratio, interpolation=cv2.INTER_AREA)
    return resizeimg

def Filter(img, value = 0):
    average = pixel_average(img)
    if value == 0:
        ret,img_filter = cv2.threshold(img, average, 255, cv2.THRESH_BINARY)
    else:
        ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
    return img_filter

def pixel_average(img):
    sum = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            sum += img[i,j]
    pixel_N = img.shape[0] * img.shape[1]
    average = sum/pixel_N
    return average

def Filter_list(imglist, value = 0):
    filterfile_list = []
    vertice_set = []
    if value == 0:
        i=0
        while i < len(imglist):
            filterfile_list.append(Filter(imglist[i]))
            #vertice_set.append(vertices(imglist[i]))
            #filterfile_list[i] = region_of_interest(filterfile_list[i], vertice_set[i])
            i+=1
    else:
        i=0
        while i < len(imglist):
            filterfile_list.append(Filter(imglist[i], value))
            #vertice_set.append(vertices(imglist[i]))
            #filterfile_list[i] = region_of_interest(filterfile_list[i], vertice_set[i])
            i+=1
    return filterfile_list

def grayscale(imglist, ratio):
    # 그레이스케일로 이미지 리드한 리스트 생성
    readfile_list = []
    i=0
    while i < len(imglist): #+ '/image seed/'
        readfile_list.append(cv2.imread(directoryname  + '/image seed/' + imglist[i], cv2.IMREAD_GRAYSCALE))
        readfile_list[i] = resize(readfile_list[i], ratio)
        i+=1
    return readfile_list

def imlistshow(imglist, name):
    i=0
    while i < len(imglist):
        cv2.imshow(name + str(i+1), imglist[i])
        i+=1



def count_pixel(img):
    number = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i,j] == 255:
                number += 1
    return number

def vertices(img): # 관심 영역 설정 - 영역 절반 할당
                   # height = img.shape[0]
                   # width = img.shape[1]
    imshape = img.shape
    lower_left = [0, imshape[0]]
    lower_right = [imshape[1], imshape[0]]
    higher_left = [0, imshape[0]/2]
    higher_right = [imshape[1], imshape[0]/2]
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


#픽셀 카운트에서 분모자리에 들어가는 인자가 0인 경우 대비 (수정) / 예외발생 방지
def pixel_ratio(img1, img2):
    temp_pixel_1 = count_pixel(img1)
    temp_pixel_2 = count_pixel(img2)
    ratio = 0
    if  temp_pixel_1 < temp_pixel_2 and temp_pixel_1 > 0:
        ratio = temp_pixel_1/temp_pixel_2
    if  temp_pixel_1 > temp_pixel_2 and temp_pixel_2 > 0:
        ratio = temp_pixel_2/temp_pixel_1
    return ratio

while True:
    capture_video_to_img()

    directoryname = os.path.dirname(os.path.realpath(__file__))

    file_list = os.listdir(directoryname + '/image seed') #

    # 그레이스케일로 이미지 리드한 리스트 생성
    print(file_list)
    readfile_list = grayscale(file_list, 0.1)
    print('그레이스케일 변환 완료')

    fltrlst = Filter_list(readfile_list)
    print('average of pixel value: ' + str(pixel_average(fltrlst[0])))
    fltrlst_ratio = pixel_ratio(fltrlst[0], fltrlst[1])
    print('f ratio: ' + str(fltrlst_ratio))
    print('img Filtering complete')
    #imlistshow(fltrlst, 'average')
    print('show')
    
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows()

