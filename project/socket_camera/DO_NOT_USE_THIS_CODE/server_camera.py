# -*- coding: utf-8 -*-
# 카메라가 연결되어 있는 서버단 파이썬 코드
# 습득된 2개의 카메라 영상을 스트리밍해줌
# Bug report : Queue 에 사진데이터를 누적하는 경우 latency가 상당히 많이 발생함.
# 바로 File Stream 형태로 소스코드 수정
# 원본 이미지 그대로 전송하는 파이썬 코드

import socket 
import numpy as np
import cv2
from _thread import *
global A,B

HOST = ''
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 
print('server start')


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    print("recv fron client")
    return buf

def get_img_channel(channel):
    message = channel
    client_socket.send(message.encode()) ## 1번 이미지 전송 요청
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    img = cv2.imdecode(data,1)
    return img

def get_gpsdata():
    message = '3'
    client_socket.send(message.encode()) ## 1번 이미지 전송 요청
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    print(stringData)

def threaded(client_socket, addr):
    while True:
        try:
            decimg1 = get_img_channel('1') # 1번 이미지 전송 요청
            cv2.imshow('SERVER CAM1',decimg1)

            decimg2 = get_img_channel('2') # 2번 이미지 전송 요청
            cv2.imshow('SERVER CAM2',decimg2)    
            key = cv2.waitKey(1)
            key = cv2.waitKey(1)
            if key == 27:
                break
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    client_socket.close() 




while True: 
    client_socket, addr = server_socket.accept() 
    threaded( client_socket, addr )

server_socket.close() 
