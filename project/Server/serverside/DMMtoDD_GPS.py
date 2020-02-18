#-*- coding:utf-8 -*-

# DMM to DD 형태로 GPS 를 변환해주는 파이썬 코드
# 여러개의 위도 및 경도를 입력하면 해당 좌표를 여러개 찍어주는 파이썬코
import folium
import os
import webbrowser
print(os.getcwd())
direction = os.getcwd()
direction += "\Test.html"
print(direction)

LATITUDE =[]
LONGITUDE =[]

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

        LATITUDE.append(CAL_latitude)
        LONGITUDE.append(CAL_longitude)
        map_osm = folium.Map(location=[LATITUDE[0], LONGITUDE[0]], zoom_start=10)
        for i in range(0,len(LATITUDE)):
            folium.Marker([LATITUDE[i], LONGITUDE[i]], popup='WAY', icon=folium.Icon(color='red',icon='info-sign')).add_to(map_osm)
            #folium.CircleMarker([37.5658859, 126.9754788], radius=100,color='#3186cc',fill_color='#3186cc', popup='덕수궁').add_to(map_osm)
        map_osm.save(direction)

while True:
        print(len(LATITUDE))
        temp_lat = float(input('latidue'))
        temp_long = float(input('longitude'))
        DMM2DD(temp_lat, temp_long)
        webbrowser.open(direction)



#한양대학교 GPS 정보
#latitude = 3733.3322
#longitude = 12702.7322 

