# -*- coding: utf-8 -*-
# 카메라가 연결되어 있는 서버단 파이썬 코드
# 습득된 2개의 카메라 영상을 스트리밍해줌
# Bug report : Queue 에 사진데이터를 누적하는 경우 latency가 상당히 많이 발생함.
# 바로 File Stream 형태로 소스코드 수정

import socket 
import cv2
import numpy
from queue import Queue
from _thread import *

global A,B
enclosure_queue = Queue()
enclosure_queue2 = Queue()

def grayscale(img): # 그레이스케일로 이미지 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 쓰레드 함수 
def threaded(client_socket, addr, queue1,queue2): 

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

        except ConnectionResetError as e:

            print('Disconnected by ' + addr[0],':',addr[1])
            break
             
    client_socket.close() 


def webcam(queue1,queue2):

    
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


HOST = '192.168.255.22'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 
print('server start')
start_new_thread(webcam, (enclosure_queue,enclosure_queue2))


while True: 
    print('wait')
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr, enclosure_queue, enclosure_queue2)) 

server_socket.close() 
