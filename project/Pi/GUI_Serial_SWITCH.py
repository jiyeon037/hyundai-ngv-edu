# -*- coding: utf-8 -*-

# pip3 install pyserial
# 파이썬에서 연결가능한 시리얼포트를 검색하고 알아서 연결함.
# 
# https://www.gpsinformation.org/dale/nmea.htm
# GPS 프로토콜 : DMM ( 도 및 십진수 분 )
import serial
from serial.tools import list_ports

# GUI 표현해주는 내용
import pygame
import time

# 서버쪽에 데이터 전
import requests

#라즈베리파이 GPIO
import RPi.GPIO as GPIO
GPIO_SIGNAL = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

pygame.init()
window = pygame.display.set_mode((1000, 656))
window.fill((255, 255, 255))
pygame.display.update()

LAT= ''
LONG=''
H=''
T=''
ALARM = ''
send_flag = False


def drow_ice_image():
    window.blit(pygame.image.load("2.png"), (0, 0))
    pygame.display.update()


def drow_image():
    window.blit(pygame.image.load("1.png"), (0, 0))
    pygame.display.update()

def DMM2DD(latitude, longitude):
        int_latitude = int(latitude)
        int_longitude = int(longitude)

        #DD = d + (min/60) + (sec/3600)
        d_latitude = int((int_latitude) / 100)
        d_longitude = int((int_longitude) / 100)

        m_latitude= (latitude -int_latitude) + int_latitude%100
        m_longitude = (longitude -int_longitude) +int_longitude%100

        CAL_latitude = d_latitude+ m_latitude/60
        CAL_longitude = d_longitude + m_longitude/60

        CAL_latitude= round(CAL_latitude,4)
        CAL_longitude= round(CAL_longitude,4)

        global LONG, LAT
        LAT = str(CAL_latitude)
        LONG = str(CAL_longitude)
        


port_lists = list_ports.comports()
for i in range(len(port_lists)):
    print(port_lists[i][0])
sel_num = 0
ser = serial.Serial(port_lists[sel_num][0],9600,timeout=1)


drow_image()

while True:
    data_list = list()
    temp_data = str(ser.readline())    
    data_list = temp_data.split(',')
    if len(data_list) == 7:
        print('LAT:{} LONG:{} H:{} T:{} ALARM : {}'.format(data_list[1],data_list[2],data_list[3],data_list[4], data_list[5]))
        DMM2DD(float(data_list[1]), float(data_list[2]))
        H = data_list[3]
        T = data_list[4]
        ALARM = data_list[5]

        
    if GPIO.input(GPIO_SIGNAL)==0 or ALARM == 'T':
        drow_image()
        pygame.display.update()
        message = 'B'
        ser.write(message.encode())

        if send_flag == False:
            send_flag = True
            print("SEND TO SERVER")
            #params = {'req_lat': LAT, 'req_lng': LONG, 'req_t1' : '10', 'req_t2' : T, 'req_h' : H}
            #response = requests.get(, params=params)
           
        
    else:
        drow_ice_image()
        send_flag = False
        pygame.display.update()


        
GPIO.cleanup()
pygame.quit()
quit()
