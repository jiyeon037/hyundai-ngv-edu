import serial
from serial.tools import list_ports
import pymysql

#def insert():
#   db_class = dbModule.Database()
#   sql = "INSERT INTO gps.location(

conn = pymysql.connect(host='localhost',user='root',password='',db='gps',charset='utf8',)
curs = conn.cursor(pymysql.cursors.DictCursor)

#sql = insert into location(latitude, longitude) values (%s,%s)

port_lists = list_ports.comports()
for i in range(len(port_lists)):
    print(port_lists[i][0])
sel_num = 0
ser = serial.Serial(port_lists[sel_num][0],9600,timeout=2)

while True:
    temp_data = str(ser.readline())
    if(temp_data.find('GPRMC') != -1):
        temp_list = list()
        temp_list = temp_data.split(',')

        if(temp_list[2]!='V'):
            sql = """insert into location(latitude, longitude) values (%s,%s)"""
            curs.execute(sql,(temp_list[3],temp_list[5]))
            conn.commit()

        print(temp_list[2])
        print(temp_list[3])
        print(temp_list[5])

