# -*- coding: utf-8 -*-
# 원격 동키카 제어 및 카메라 스트리밍 코드
# 동키카는 흑백 영상을 Streaming
'''
2020.02.12
동키카 PWM / STREAMING + 외부 연산장치 연산결과에 따른 GPIO 출력
노면 상태가 젖은 경우 라즈베리파이 GPIO 21 번이 HIGH 상태가 되었다가 특정 시간이 지난 뒤에 자동으로 LOW됨


'''
import cv2
import numpy
import time
import pygame
import socket
import time
import RPi.GPIO as GPIO
from _thread import *

#라즈베리파이 GPIO
import RPi.GPIO as GPIO
GPIO_SIGNAL = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(GPIO_SIGNAL,False)




import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685() #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
pwm.set_pwm_freq(60) # 서보모터 60Hz로 펄스주기를 설정.

#### 동키카 PWM 펄스 조절 부분 #########
# 이 부분의 값을 적절히 조절해서 전진/후진/정지/좌/우 조절할 것#
PWM_GO   = 395
PWM_BACK = 370
PWM_STOP = 380

PWM_LEFT = 260
PWM_RIGHT  = 500
PWM_CENTER = 380
#### 동키카 PWM 펄스 조절 부분 #########



# Settings for joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 3                       # 라즈베리파이에서는 3 / 컴퓨터에서는 4로 지정하면 됨
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

HOST = ''
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 
print('server start')


A =b'hello'
B =b'world'
global GO
global TILT
global CONT_DATA
GO = 0
TILT = 0
tt =1

ALARM = False
init_time = time.time()

#PCA9685 관련 펄스 초기설정 함수 
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
    pwm.set_pwm_freq(60)


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
        
# 그레이스케일로 이미지 변환
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

## time.sleep의 system 독점을 방지하기 위한 내용
def millis_python():
    now_time = time.time()
    now_time = (now_time - init_time)
    return now_time

# 쓰레드 함수  ( 소켓 통신 개시 이후 무한 loop 문 처럼 작동하는 구문 )
def threaded(client_socket, addr):
    global tt
    print('Connected by :', addr[0], ':', addr[1]) 
    stringData = b''
    while True: 
        try:
            data = client_socket.recv(1024)
            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break
            ch_data = int(data)
            if ch_data == 1:
                stringData = A
                #stringData = queue1.get()
            if ch_data == 2:
                stringData = B
                #stringData = queue2.get()
            if ch_data == 3:                           ### WARN SIGNAL
                GPIO.output(GPIO_SIGNAL,False)
                stringData = ''
                print("EEEE")
                tt = millis_python()
            
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.send(stringData)
            ## 이 부분에 PWM 제어 신호 넣으면 됨
            CONT_DATA = PygameHandler(pygame.event.get())
            print(GO, TILT)
            if GO == 1:
                print("FORWARD")
                pwm.set_pwm(0, 0, PWM_GO) #0번서보
            elif GO == -1:
                print("BACKWARD")
                pwm.set_pwm(0, 0, PWM_BACK) #0번서보
            else:                      # 이 부분에 전진모터 중립
                pwm.set_pwm(0, 0, PWM_STOP) #0번서보

            if TILT == 1:
                print("LEFT")
                pwm.set_pwm(3, 0, PWM_LEFT) #3번서보
            elif TILT == -1:
                print("RIGHT")
                pwm.set_pwm(3, 0, PWM_RIGHT) #3번서보
            else:                      # 이 부분에 조향서보모터 중립
                pwm.set_pwm(3, 0, PWM_CENTER) #3번서보   

            ## 특정 시간이 지나면 자동으로 알람을 해제하는 부분 ( 5초 이상 경과 시 OFF )
            if (millis_python() - tt > 5):
                GPIO.output(GPIO_SIGNAL,True)
                ALARM = False
            
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break             
    client_socket.close() 


def webcam():
    capture1 = cv2.VideoCapture(0) # 카메라 채널 바꿔주면 됨
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
            A = stringData1
            cv2.imshow('CH1', frame1)

        if ret2 == True:       
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
            frame2 = grayscale(frame2)
            result, imgencode = cv2.imencode('.jpg', frame2, encode_param)
            data2 = numpy.array(imgencode)
            stringData2 = data2.tostring()
            B = stringData2
            cv2.imshow('CH2', frame2)
        key = cv2.waitKey(1)
        if key == 27:
            break

GPIO.output(GPIO_SIGNAL,True)

start_new_thread(webcam, ())
        
while True:
    print('wait')
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr )) 

server_socket.close() 
GPIO.cleanup()        
                

