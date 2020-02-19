# -*- coding: utf-8 -*-
# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np
import socket


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
 
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def get_img_channel(channel):
    message = channel
    client_socket.send(message.encode()) ## 1번 이미지 전송 요청
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    img = cv2.imdecode(data,1)
    return img
 

#에그 HOST = '192.168.255.22'
HOST = '192.168.0.7'
PORT = 9999
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 

while True:
    frame1 = get_img_channel('1')
    frame2 = get_img_channel('2')
    if True:
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


        show_frame1= im_trim1(grayA) #trim_image 변수에 결과물을 넣는다
        show_frame2= im_trim2(grayB)

        cv2.imshow("CAM1", show_frame1)
        cv2.imshow("CAM2", show_frame2)
        
        (score, diff) = compare_ssim(show_frame1, show_frame2, full=True)
        diff = (diff * 255).astype("uint8")

        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        nzCount = cv2.countNonZero(thresh)
        nzCount_percent = nzCount / (h*w)
        print("Thresh: {}  SSIM: {} numbers {} percent {} ".format(thresh, score , nzCount,nzCount_percent))

         

cv2.destroyAllWindows() # 리소스 반환
cv2.waitKey(0)
client_socket.close()
