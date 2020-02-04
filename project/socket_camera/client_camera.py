Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@ROHYUNSEOK 
Learn Git and GitHub without any code!
Using the Hello World guide, you’ll start a branch, write comments, and open a pull request.


jiyeon037
/
project
1
00
 Code Issues 0 Pull requests 0 Actions Projects 0 Wiki Security Insights
project/project/socket_camera/client_camera.py / 
@ROHYUNSEOK ROHYUNSEOK ROH:test update
a6253aa yesterday
54 lines (43 sloc)  1.4 KB
  
Code navigation is available!
Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more

You're using code navigation to jump to definitions or references.
Learn more or give us feedback
# -*- coding: utf-8 -*-
# 소켓 통신으로 다중 웹캠 정보를 받아오는 파이썬 코드
# 서버코드가 먼저 실행뒤에 클라이언트 코드를 실행할 것
# GPS 추가 
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

def get_gpsdata():
    message = '3'
    client_socket.send(message.encode()) ## 1번 이미지 전송 요청
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    print(stringData)

HOST = '192.168.0.7'
PORT = 9999
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 


while True:    
    decimg1 = get_img_channel('1') # 1번 이미지 전송 요청
    cv2.imshow('CH1 CAM',decimg1)

    decimg2 = get_img_channel('2') # 2번 이미지 전송 요청
    cv2.imshow('CH2 CAM',decimg2)

    #/get_gpsdata()
   
    
    key = cv2.waitKey(1)
    if key == 27:
        break
client_socket.close() 
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
