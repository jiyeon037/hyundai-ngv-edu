# -*- coding: utf-8 -*-
# 소켓 통신으로 다중 웹캠 정보를 받아오는 파이썬 코드
# 서버코드가 먼저 실행뒤에 클라이언트 코드를 실행할 것
# GPS 추가 
import socket 
import numpy as np
import cv2
import time
from _thread import *

A = b''
B = b''

from _thread import *
HOST = '192.168.0.5'
#HOST = '192.168.255.22'
PORT = 9999


# 쓰레드 함수 
def threaded(): 
    while True: 
        if  True:
            data = client_socket.recv(1024)
            if not data: 
                break
            stringData = b''
            ch_data = int(data)
            if ch_data == 1:
                print("1 recv")
                stringData = A
                
            if ch_data == 2:
                print("2 recv")
                stringData = B
            if len(stringData) > 0:
                client_socket.send(str(len(stringData)).ljust(16).encode())
                client_socket.send(stringData)
            else:
                print("size err")
                


def webcam(break_flag):   
    capture1 = cv2.VideoCapture(0) # 카메라 채널 바꿔주면 됨
    capture2 = cv2.VideoCapture(1) # 카메라 채널 바꿔주면 됨
    while True:
        ret1, frame1 = capture1.read()
        ret2, frame2 = capture2.read()
        if ret1 == True:       
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            result, imgencode = cv2.imencode('.jpg', frame1, encode_param)
            data1 = np.array(imgencode)
            stringData1 = data1.tostring()
            global A
            A = stringData1
        else:
            frame1 = np.zeros((512,512,3)) #카메라 준비 안됨
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            result, imgencode = cv2.imencode('.jpg', frame1, encode_param)
            data1 = np.array(imgencode)
            stringData1 = data1.tostring()
            A = stringData1
            print("CAM NOT READY")
        
            
        if ret2 == True:       
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            result, imgencode = cv2.imencode('.jpg', frame2, encode_param)
            data2 = np.array(imgencode)
            stringData2 = data2.tostring()
            global B
            B = stringData2
        else:
            frame1 = np.zeros((512,512,3)) #카메라 준비 안됨
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            result, imgencode = cv2.imencode('.jpg', frame22, encode_param)
            data2 = np.array(imgencode)
            stringData2 = data2.tostring()
            B = stringData2
            print("CAM NOT READY")
            
        key = cv2.waitKey(1)
        if key == 27:
            break
        if break_flag == True:
            break
        cv2.imshow('CH1', frame1)
        cv2.imshow('CH2', frame2)

for i in range(3):
    print("CAM HEAT")
    webcam(True)
break_falg =False

start_new_thread(webcam, (break_falg,))
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 
print("CONNECT")


while True:
    start_new_thread(threaded, ())
     #print(' LEN {} '.format(str(len(A)) ))
