# -*- coding: utf-8 -*-
# 소켓 통신으로 다중 웹캠 정보를 받아오는 파이썬 코드
# 서버코드가 먼저 실행뒤에 클라이언트 코드를 실행할 것
import socket 
import numpy as np
import cv2


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


HOST = '192.168.255.25'
PORT = 9999
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 


while True:    
    decimg1 = get_img_channel('1') # 1번 이미지 전송 요청
    cv2.imshow('CH1 CAM',decimg1)

    decimg2 = get_img_channel('2') # 2번 이미지 전송 요청
    cv2.imshow('CH2 CAM',decimg2)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
client_socket.close() 
