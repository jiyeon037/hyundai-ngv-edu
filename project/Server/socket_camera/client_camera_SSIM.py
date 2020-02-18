# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np
import socket 

def grayscale(img): # 흑백 이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

video_caputre_1 = cv2.VideoCapture(0) # 외장형 USB 웹캠1
video_caputre_2 = cv2.VideoCapture(1) # 외장형 USB 웹캠2

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


HOST = '192.168.0.7'
PORT = 9999
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 


def im_trim1(img): #함수로 만든다
    x = 60; y = 155; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    img_trim1 = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다
    #cv2.imwrite('org_trim.jpg',img_trim) #org_trim.jpg 라는 이름으로 저장
    return img_trim1 #필요에 따라 결과물을 리턴

def im_trim2(img): #함수로 만든다
    x = 80; y = 100; #자르고 싶은 지점의 x좌표와 y좌표 지정
    w = 200; h = 200; #x로부터 width, y로부터 height를 지정
    img_trim2 = img[y:y+h, x:x+w] #trim한 결과를 img_trim에 담는다
    #cv2.imwrite('org_trim.jpg',img_trim) #org_trim.jpg 라는 이름으로 저장
    return img_trim2 #필요에 따라 결과물을 리턴

def grayscale(img): # 그레이스케일로 이미지 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def pixel_value_average(img): # 픽셀 값의 평균 계산
    sum = 0
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            sum += img[i,j]
    pixel_N = img.shape[0] * img.shape[1]
    average = sum/pixel_N
    return average

def Filter(img, value = 0): # 픽셀 값 평균을 기준으로 필터링
    average = pixel_value_average(img)

    if value == 0:
        ret,img_filter = cv2.threshold(img, average*0.7, 255, cv2.THRESH_BINARY)
    else:
        ret,img_filter = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
       
    return img_filter

while True:
    frame1 = get_img_channel('1')# 1번 이미지 전송 요청
    frame2 = get_img_channel('2') # 2번 이미지 전송 요청

    if True:
        (h, w) = frame1.shape[:2]
        (h, w) = frame2.shape[:2]

# calculate the center of th
        center = (w/3 , h/1.5)
 
        angle90 = 90
        angle180 = 180
        angle270 = 270
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle90, scale)
        rotated901 = cv2.warpAffine(frame1, M, (h, w))
        M = cv2.getRotationMatrix2D(center, angle90, scale)
        rotated902 = cv2.warpAffine(frame2, M, (h, w))
        
        grayA = cv2.cvtColor( rotated901, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(rotated902, cv2.COLOR_BGR2GRAY)
        
        asd= im_trim1(grayA)#trim_image 변수에 결과물을 넣는다
        qwe= im_trim2(grayB)

        img1 = Filter(asd)
        img2 = Filter(qwe)

        nzCount1 = cv2.countNonZero(img1)
        nzCount2 = cv2.countNonZero(img2)

        cv2.imshow("CAM1", img1)
        cv2.imshow("CAM2", img2)
        cv2.imshow("origin", asd)
        
        #(score, diff) = compare_ssim(asd, qwe, full=True)
        #diff = (diff * 255).astype("uint8")

        #thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        #cv2.imshow("Thresh", thresh)

        #print("SSIM: {}".format(score))
        
       

        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 사용자가 키보드 q 누르면 OpenCV 종료



video_caputre_1.release()
video_caputre_2.release()


cv2.destroyAllWindows() # 리소스 반환
cv2.waitKey(0)
client_socket.close() 
