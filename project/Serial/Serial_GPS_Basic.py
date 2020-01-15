# pip3 install pyserial
# 파이썬에서 연결가능한 시리얼포트를 검색하고 알아서 연결함.
# 
# https://www.gpsinformation.org/dale/nmea.htm
# GPS 프로토콜 : DMM ( 도 및 십진수 분 )
import serial
from serial.tools import list_ports

port_lists = list_ports.comports()
for i in range(len(port_lists)):
    print(port_lists[i][0])
sel_num = 0
ser = serial.Serial(port_lists[sel_num][0],9600,timeout=2)

while True:
    temp_data = str(ser.readline())
    if(temp_data.find('GPRMC') != -1):
        #print(temp_data)
        temp_list = list()
        temp_list = temp_data.split(',')
        print(temp_list[2]) # V : GPS unstable/ A : stable
        
