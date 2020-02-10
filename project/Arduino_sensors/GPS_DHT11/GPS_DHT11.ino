#include <SoftwareSerial.h>
SoftwareSerial GPS(7,6);
String GPS_DATA;
unsigned long GPS_LAST;

#include "DHT.h"
#define DHTPIN 2  //온습도 센서 디지털 2번에 신호선 연결
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

      String lattitude;
      String longitude;
      int hum;
      int temp;

void setup() {
  // put your setup code here, to run once:
  GPS.begin(9600);
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(GPS.available())
  {
    char data;
    data = GPS.read();
    GPS_DATA += data;
    GPS_LAST = millis();
  }
  if(!GPS.available() && millis() - GPS_LAST > 100)
  {
    //Serial.print(GPS_DATA);
    int data_start = GPS_DATA.indexOf("GPRMC");
    int data_end   = GPS_DATA.indexOf("GPVTG");
    if(data_start >0 && data_end >0)// 유효 데이터 확인
    {
        //Serial.print(data_start); Serial.print("  "); Serial.println(data_end);
      GPS_DATA = GPS_DATA.substring(data_start, data_end);
        //Serial.println(GPS_DATA);
      int first_comma    = GPS_DATA.indexOf(",");
      int second_comma   = GPS_DATA.indexOf(",", first_comma+1);
      int third_comma    = GPS_DATA.indexOf(",", second_comma+1);
      int fourth_comma   = GPS_DATA.indexOf(",", third_comma+1);
      int fifth_comma    = GPS_DATA.indexOf(",", fourth_comma+1);
      int sixth_comma    = GPS_DATA.indexOf(",", fifth_comma+1);
      
      lattitude = GPS_DATA.substring(third_comma+1, fourth_comma); //위도 
      longitude = GPS_DATA.substring(fifth_comma+1, sixth_comma);  //경도 
        //GPRMC,000505.021,V,,,,,0.00,0.00,060180,,,N*41
    }
    GPS_DATA = "";
    hum = dht.readHumidity();      //대기습도
    temp = dht.readTemperature();  //대기온도
    // 이 부분에 적외선 온도 센서 시작 



    // 이 부분에 적외선 온도 센서 끝
    
    // 라즈베리파이에 정보 송신
    Serial.print("A ,");
    Serial.print(lattitude); Serial.print(",");
    Serial.print(longitude); Serial.print(",");
    Serial.print(hum);       Serial.print(",");
    Serial.print(temp);      Serial.print(",");
    Serial.println();
  }
}
