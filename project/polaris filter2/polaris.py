# made by junse
import os
import cv2
import numpy as np

def resize(img, ratio, dsize=None, dst=None):
    resizeimg = cv2.resize(img, dsize, dst, ratio, ratio, interpolation=cv2.INTER_AREA)
    return resizeimg

def Filter(img, value):
    img_filter = np.copy(img)

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img[i,j] < value:
                img_filter[i,j] = 0
            else:
                img_filter[i,j] = 255

    return img_filter

def Filter_list(imglist, value):
    filterfile_list = []
    i=0
    while i < len(imglist):
        filterfile_list.append(Filter(imglist[i], value))
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

def imlistshow(imglist):
    i=0
    while i < len(imglist):
        cv2.imshow(str(i+1), imglist[i])

        filename = 'filtering'+str(i+1)+'.jpg'
        cv2.imwrite(directoryname + '/image_save/' + filename, imglist[i])
        i+=1


directoryname = os.path.dirname(os.path.realpath(__file__))

file_list = os.listdir(directoryname + '/image seed')

# 그레이스케일로 이미지 리드한 리스트 생성

readfile_list = grayscale(file_list, 0.5)

print('그레이스케일 변환 완료')

filterfile_list = Filter_list(readfile_list, 120)
#vertical = cv2.imread(directoryname+'/1.jpg', cv2.IMREAD_GRAYSCALE)
#horizon = cv2.imread(directoryname+'/2.jpg', cv2.IMREAD_GRAYSCALE)
print('img read complete')

#vertical = resize(vertical, 0.5)
#horizon = resize(horizon, 0.5)
print('img resize complete')


#vertical_F = Filter(vertical, 150)
#horizon_F = Filter(horizon, 150)
print('img reinforce complete')
imlistshow(filterfile_list)
print('show')



#cv2.imshow('v', filterfile_list)
#cv2.imshow('h', horizon_F)
cv2.waitKey(0)
cv2.destroyAllWindows()