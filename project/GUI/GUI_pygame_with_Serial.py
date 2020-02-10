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

pygame.init()
window = pygame.display.set_mode((1000, 656))
window.fill((255, 255, 255))
pygame.display.update()
def drow_ice_image():
    window.blit(pygame.image.load("car_ice_icon.png"), (0, 0))
    pygame.display.update()


def drow_image():
    window.blit(pygame.image.load("car_no_icon.png"), (0, 0))
    pygame.display.update()



port_lists = list_ports.comports()
for i in range(len(port_lists)):
    print(port_lists[i][0])
sel_num = 0
ser = serial.Serial(port_lists[sel_num][0],9600,timeout=1)


drow_image()

while True:
    '''
    print("A")
    drow_image()
    time.sleep(1)

    print("B")
    drow_ice_image()
    time.sleep(1)
    pygame.display.update()
    '''
    data_list = list()
    temp_data = str(ser.readline())    
    data_list = temp_data.split(',')
    if len(data_list) == 5:
        print('LAT:{} LONG:{} H:{} T:{}'.format(data_list[0],data_list[1],data_list[2],data_list[3]))

pygame.quit()
quit()
