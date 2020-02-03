import cv2
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def Filter(img, value):
    ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_OTSU)
    return img_filter

def pixel_value_average(img):
    sum = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            sum += img[i,j]
    pixel_N = img.shape[0] * img.shape[1]
    average = sum/pixel_N
    return average

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    
    if (ret1):
        frame1 = grayscale(frame1)
        frame1 = Filter(frame1, 150)
        cv2.imshow("CAM1", frame1)
        
    if (ret2):
        frame2 = grayscale(frame2)
        frame2 = Filter(frame2, 150)
        cv2.imshow("CAM2", frame2)
        
    if cv2.waitKey(1) & 0xFF == 27:
        break
    #esc
    
cap1.release()
cap2.release()

cv2.destroyAllWindows()
