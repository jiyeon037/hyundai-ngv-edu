# -*- coding: utf-8 -*-
# 원격 동키카 제어 및 카메라 스트리밍 코드
# 원본 영상 스트리밍 ( 흑백 )
import cv2
import numpy
import time
import pygame
import socket 
from _thread import *



# Settings for joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 3                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

HOST = '192.168.255.22'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 
print('server start')


global A,B
global GO
global TILT
global CONT_DATA
GO = 0
TILT = 0 

# Function to handle pygame events
def PygameHandler(events):
    #조이스틱 이벤트 발생한 경우
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            global GO
            global TILT
            if upDown < -0.1:
                #print("GO")
                GO = 1
            elif upDown > 0.1:
                #print("BACK")
                GO = -1
            else:
                GO = 0

            if leftRight < -0.1:
                #print("LEFT")
                TILT = 1
            elif leftRight > 0.1:
                #print("RIGHT")
                TILT = -1
            else:
                TILT = 0
                
            return GO, TILT

def grayscale(img): # 그레이스케일로 이미지 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 쓰레드 함수  ( 소켓 통신 개시 이후 무한 loop 문 처럼 작동하는 구문 )
def threaded(client_socket, addr): 
    print('Connected by :', addr[0], ':', addr[1]) 
    while True: 
        try:
            data = client_socket.recv(1024)
            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break
            ch_data = int(data)
            if ch_data == 1:
                global A
                stringData = A
                #stringData = queue1.get()
            if ch_data == 2:
                global B
                stringData = B
                #stringData = queue2.get()
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.send(stringData)
            ## 이 부분에 PWM 제어 신호 넣으면 됨
            CONT_DATA = PygameHandler(pygame.event.get())
            print(GO, TILT)
            if GO == 1:
                print("FORWARD")
            elif GO == -1:
                print("BACKWARD")
            #else: # 이 부분에 전진모터 중립

            if TILT == 1:
                print("LEFT")
            elif TILT == -1:
                print("RIGHT")
            #else: # 이 부분에 조향서보모터 중립
                
            
            
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break             
    client_socket.close() 


def webcam():
    capture1 = cv2.VideoCapture(1) # 카메라 채널 바꿔주면 됨
    capture2 = cv2.VideoCapture(2) # 카메라 채널 바꿔주면 됨
    while True:
        ret1, frame1 = capture1.read()
        ret2, frame2 = capture2.read()
        if ret1 == True:       
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            frame1 = grayscale(frame1)
            result, imgencode = cv2.imencode('.jpg', frame1, encode_param)
            data1 = numpy.array(imgencode)
            stringData1 = data1.tostring()
            #queue1.put(stringData1)
            global A
            A = stringData1
            cv2.imshow('CH1', frame1)

        if ret2 == True:       
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            frame2 = grayscale(frame2)
            result, imgencode = cv2.imencode('.jpg', frame2, encode_param)
            data2 = numpy.array(imgencode)
            stringData2 = data2.tostring()
            #queue2.put(stringData2)
            global B
            B = stringData2
            cv2.imshow('CH2', frame2)
        key = cv2.waitKey(1)
        if key == 27:
            break


start_new_thread(webcam, ())
        
while True:
    print('wait')
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr )) 

server_socket.close() 
        
                
                
