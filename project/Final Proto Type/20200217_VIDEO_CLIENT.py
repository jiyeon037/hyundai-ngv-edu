import os
import cv2
import numpy as np
import math
import time
import sys
import socket
WARN_FLAG = False

'''
1. 웹캠 이미지 리드
2. ROI 설정
3. 픽셀 값의 평균으로 필터링: 평균값보다 크면 255(white), 작으면 0(black)
4. 설정한 unit 크기로 이미지를 분할해 각각의 픽셀 수 차이 계산
5. wet으로 판단되는 unit을 box로 표시
6. box의 갯수가 일정 값 이상이면 count: while문으로 순환하기 때문에 count를 세서 지속적으로 wet일때만 젖은 도로라고 판단
7. count가 일정 값 이상이면 'WET ROAD DETECTED' 출력
'''
'''
wet 판단 기준
# unit의 ratio값이 일정값 이하
# 인접한 unit의 ratio값 차이가 일정값 이상
# 위의 두 조건을 만족하면서 unit이 2*2 이상으로 밀집되어있을 때
'''
'''
설정해야 하는 변수
# Threshold 값(TH)
# image trim의 x,y 값
# 이미지를 분할할 unit의 크기: 300*300 이미지 이므로 unit은 300의 약수
# wet_point_list 함수의 ref1, ref2
'''

def im_trim(img, x, y, w, h): # 분석 가능한 이미지로 ROI 설정

    (a, b) = img.shape[:2]
    center = (b/3 , a/1.5)
    angle90 = 90
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle90, scale)
    img = cv2.warpAffine(img, M, (a, b))
    '''
    x = 100; y = 100; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    '''
    img_trim = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다

    return img_trim

def grayscale(img): # 그레이스케일로 이미지 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def Filter(img, value = 0): # 픽셀 값 평균을 기준으로 필터링
    average = img.mean()

    if value == 0:
        ret,img_filter = cv2.threshold(img, average, 255, cv2.THRESH_BINARY)
    else:
        ret,img_filter = cv2.threshold(img, average*value, 255, cv2.THRESH_BINARY)
        #ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
       
    return img_filter

def count_pixel(img): # 픽셀 값이 0인 픽셀 COUNT
    number = cv2.countNonZero(img)

    return number

def pixel_ratio0(img1, img2): # 픽셀 값 0 비율 계산
    ratio = 1-abs((count_pixel(img2)-count_pixel(img1))/img1.size)
    return ratio*100

def same_bright(frame, gap): # 두 이미지의 밝기를 동일하게 조절
    if gap>=0:
        M = np.ones(frame.shape, dtype = "uint8") * abs(int(gap))
        transform = cv2.add(frame, M)
    else:
        M = np.ones(frame.shape, dtype = "uint8") * abs(int(gap))
        transform = cv2.subtract(frame, M)
    
    return transform

def seperated_image_ratio(frame1, frame2, unit): #unit의 수만큼 이미지를 분할하여 분할된 이미지의 pixel_ratio를 array에 저장
    ratio_arr = np.zeros((unit,unit), dtype = int)
    U = int(frame1.shape[0]/unit)
    white = (255,255,255)
    black = (0,0,0)

    # 격자 그리기
    for x in range(unit): cv2.line(frame2, (U*x, 0), (U*x, U*unit), black, 1, 4)
    for y in range(unit): cv2.line(frame2, (0, U*y), (U*unit, U*y), black, 1, 4)

    # ratio 행렬 생성
    for i in range(unit):
        for j in range(unit):
            img_trim1 = frame1[i*U:(i+1)*U, j*U:(j+1)*U]
            img_trim2 = frame2[i*U:(i+1)*U, j*U:(j+1)*U]
            ratio = int(pixel_ratio0(img_trim1, img_trim2))
            ratio_arr[i,j] = ratio

            # unit의 좌표 값과 ratio값 이미지에 표시

            text = '('+str(i)+','+str(j)+')'
            #cv2.putText(frame2, text, (j*U+int(U*0.2), i*U+int(U*0.4)), 1, 0.5, black)
            cv2.putText(frame2, str(ratio), (j*U+int(U*0.3), i*U+int(U*0.8)), 1, 0.6, black)
           
    return ratio_arr           

def wetpoint_list(r_arr): # 1. 각각의 unit의 인접한 unit의 ratio값의 차가 일정 값을 넘으면 wet list에 좌표 값 저장
                          # 2. unit의 ratio값이 일정 값을 넘으면 wet list에 좌표 값 저장 

    wet = []
    ref1 = 25 # 인접한 unit간 ratio차이의 기준값
    ref2 = 50 # unit의 ratio 기준값
    for i in range(len(r_arr[0])):
        for j in range(len(r_arr[1])):

            R = r_arr[i,j]
                
            Rlst = []
            if (1<=i<=len(r_arr[0])-2 and 1<=j<=len(r_arr[1])-2):
                for m in range(3):
                    for n in range(3):
                        Rlst.append(r_arr[i-1+m,j-1+n])
            for r in Rlst:
                if r-R > ref1:
                    wet.append((i,j))
                if wet != []:
                    if wet[-1] == (i,j):
                        break
            
            if wet != []:
                if wet[-1] != (i,j):
                    if np.mean(r_arr)-R > ref2 and R!=0:
                        wet.append((i,j))
    return wet

def wet_list_filter(arr, wet): # wet리스트의 좌표값을 r_arr와 같은 크기의 2차원 array의 좌표에 1로 표시
                               # 2*2구역의 값이 모두 1이면 wet_lst에 좌표값 저장

    wet_arr = np.zeros(arr.shape, dtype = int)
    wet_lst = []

    # wet 리스트의 좌표 값을 wet_arr에 1로 표시
    for n in wet:
        x = n[1]
        y = n[0]
        wet_arr[x,y] = 1
    
    #2*2 구역의 값이 모두 1이면 wet_lst에 좌표값 저장
    for i in range(len(arr[0])):
        for j in range(len(arr[1])):
            if i+1<len(arr[0])-1 and j+1<len(arr[1])-1:
                if wet_arr[i,j]*wet_arr[i+1,j]*wet_arr[i,j+1]*wet_arr[i+1,j+1] == 1:
                   wet_lst.append((i,j))
                   wet_lst.append((i+1,j))
                   wet_lst.append((i,j+1))
                   wet_lst.append((i+1,j+1))
    
    wet_lst = list(set(wet_lst))

    return wet_lst

def boxing_wet(frame, lst, unit): # wet list의 젖은 픽셀 좌표를 box로 화면에 표시
    U = int(frame.shape[0]/unit)
    thick = 2
    for n in lst:
        x = n[0]
        y = n[1]
        cv2.line(frame, (U*x, U*y), (U*x, U*(y+1)), (0,0,255), thick, 4)
        cv2.line(frame, (U*x, U*y), (U*(x+1), U*y), (0,0,255), thick, 4)
        cv2.line(frame, (U*(x+1), U*y), (U*(x+1), U*(y+1)), (0,0,255), thick, 4)
        cv2.line(frame, (U*x, U*(y+1)), (U*(x+1), U*(y+1)), (0,0,255), thick, 4)

def nothing(x):
    pass #더미 함수 생성... 트랙 바 생성시 필요하므로

def recvall(sock, Count):
    buf = b''
    while Count:
        newbuf = sock.recv(Count)
        if not newbuf: return None
        buf += newbuf
        Count -= len(newbuf)
    return buf

def SEND_WARN():
    for i in range(3):
        Message = '3'
        client_socket.send(Message.encode()) ##알람 경보 활성화  
        print("send")
        length = recvall(client_socket,16)
        stringData = recvall(client_socket, int(length))

def SEND_SAFE():
    Message = '4'
    client_socket.send(Message.encode()) ##알람 경보 활성화  
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    


def get_img_channel(channel):
    message = channel
    client_socket.send(message.encode()) ## 1번 이미지 전송 요청
    length = recvall(client_socket,16)
    stringData = recvall(client_socket, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    img = cv2.imdecode(data,1)
    return img

HOST = '192.168.0.9'
PORT = 9999
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 

cv2.namedWindow('Binary') #트랙바를 붙일 윈도우를 생성
cv2.resizeWindow('Binary', 400, 120)
cv2.createTrackbar('threshold','Binary', 0, 150, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('threshold', 'Binary', 100) #초기값 100
cv2.createTrackbar('X','Binary', 0, 100, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('X', 'Binary', 40) #초기값 40
cv2.createTrackbar('Y','Binary', 150, 250, nothing) #트랙바를 이름이'Binary'인 윈도우에 붙임'
cv2.setTrackbarPos('Y', 'Binary', 200) #초기값 200

count = 0
unit = 15 #pixel이 300*300 이므로 unit은 300의 약수여야함
f1 =''
f2 =''
while True:
    if WARN_FLAG == True:
        SEND_WARN()
        WARN_FLAG = False
        
    f1 = get_img_channel('1') # 1번 이미지 전송 요청
    f2 = get_img_channel('2') # 2번 이미지 전송 요청
    
    TH = cv2.getTrackbarPos('threshold','Binary')*0.01 # threshold 필터링 값ㅂ
    x = cv2.getTrackbarPos('X','Binary') # frame2의 x축 값 변경
    y = cv2.getTrackbarPos('Y','Binary') # frame2의 y축 값 변경

    if  True:
        frame1_rgb = im_trim(f1, 72, 100, 300, 300)
        frame2_rgb = im_trim(f2, x, y, 300, 300) # x 초기값 40, y 초기값 200

        frame1 = grayscale(frame1_rgb)
        frame2 = grayscale(frame2_rgb)

        average1 = frame1.mean()
        average2 = frame2.mean()
        gap = average1 - average2

        frame2_c = same_bright(frame2, gap)
        
        average2_c = frame2_c.mean()

        thresh1 = Filter(frame1, TH)
        thresh2 = Filter(frame2_c, TH)

        thresh3 = cv2.bitwise_xor(thresh1, thresh2) # t1, t2 이미지 겹치는 부분 0으로 변환
        xor_ratio = count_pixel(thresh3) * 100/ thresh3.size

        unit_arr = seperated_image_ratio(thresh1, thresh2, unit)  
        p_ratio = int(np.mean(unit_arr))

        wet = wetpoint_list(unit_arr)
        wet = wet_list_filter(unit_arr, wet)
        boxing_wet(frame1_rgb, wet, unit)
       
        if len(wet) > 3:
            count += 1
        else:
            count = 0
        
        sign = 0
        if count > 10: ## 노면이 젖은 부분을 검출하는 부분
            sign = 1

            print('',\
            'W.P '+str(len(wet)),\
            'R: '+ str(p_ratio),\
            'TH: ' + str(TH),\
            'GAP: ' + str(int(gap)),\
            'A1: ' + str(int(average1)),\
            'XOR: ' + str(int(xor_ratio)),\
            'COUNT: ' + str(count),\
            'WET ROAD DETECTED!!!',\
            '',\
            sep = ' | ')
            wet = []
            WARN_FLAG = True
            

        else:
            SEND_SAFE()
            print('',\
            'W.P '+str(len(wet)),\
            'R: '+ str(p_ratio),\
            'TH: ' + str(TH),\
            'GAP: ' + str(int(gap)),\
            'A1: ' + str(int(average1)),\
            'XOR: ' + str(int(xor_ratio)),\
            'COUNT: ' + str(count),\
            '',\
            sep = ' | ')

        cv2.imshow("1", thresh1)
        cv2.imshow("2", thresh2)
        cv2.imshow('55', f2)
        #cv2.imshow("3", thresh3)
        cv2.imshow("ORIGIN1", frame1_rgb)
        #cv2.imshow("ORIGIN2", frame2_c)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 Opencv 종료

cv2.destroyAllWindows() # 리소스 반환
cv2.waitKey(0)
client_socket.close() 
