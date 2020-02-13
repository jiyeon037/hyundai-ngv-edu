# made by junse
import os
import cv2
import numpy as np

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

    return img_filter

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
    while i < len(imglist):
        readfile_list.append(cv2.imread(directoryname + '/image seed/' + imglist[i], cv2.IMREAD_GRAYSCALE))
        readfile_list[i] = resize(readfile_list[i], ratio)
        i+=1
    return readfile_list

def imlistshow(imglist, name):
    i=0
    while i < len(imglist):
        cv2.imshow(name + str(i+1), imglist[i])
        i+=1

def pixel_average(img):
    sum = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            sum += img[i,j]
    pixel_N = img.shape[0] * img.shape[1]
    average = sum/pixel_N
    return average

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

def pixel_ratio(img1, img2):
    
    if count_pixel(img1) < count_pixel(img2):
        ratio = count_pixel(img1)/count_pixel(img2)
    else:
        ratio = count_pixel(img2)/count_pixel(img1)
    return ratio


directoryname = os.path.dirname(os.path.realpath(__file__))

file_list = os.listdir(directoryname + '/image seed')

# 그레이스케일로 이미지 리드한 리스트 생성

readfile_list = grayscale(file_list, 1)
print('그레이스케일 변환 완료')

fltrlst = Filter_list(readfile_list)
print('average of pixel value: ' + str(pixel_average(fltrlst[0])))

fltrlst_ratio = pixel_ratio(fltrlst[0], fltrlst[1])

print('f ratio: ' + str(fltrlst_ratio))

print('img Filtering complete')

imlistshow(fltrlst, 'average')

print('show')

cv2.waitKey(0)
cv2.destroyAllWindows()