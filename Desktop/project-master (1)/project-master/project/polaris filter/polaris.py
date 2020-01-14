#made by junse
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



directoryname = os.path.dirname(os.path.realpath(__file__))
vertical = cv2.imread(directoryname+'\polaris_vertical.jpg', cv2.IMREAD_GRAYSCALE)
horizon = cv2.imread(directoryname+'\polaris_horizon.jpg', cv2.IMREAD_GRAYSCALE)
print('img read complete')

vertical = resize(vertical, 0.2)
horizon = resize(horizon, 0.2)
print('img resize complete')

vertical_F = Filter(vertical, 200)
horizon_F = Filter(horizon, 200)
print('img reinforce complete')

cv2.imshow('v', vertical_F)
cv2.imshow('h', horizon_F)
cv2.waitKey(0)
cv2.destroyAllWindows()