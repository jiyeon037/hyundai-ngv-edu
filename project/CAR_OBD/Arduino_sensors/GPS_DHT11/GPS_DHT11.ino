#include <SoftwareSerial.h>
SoftwareSerial GPS(7,6);
String GPS_DATA;
String BT_DATA;
boolean BT_FLAG;

String RASP_DATA;
boolean RASP_FLAG;

boolean ALARM_FLAG,SEND_FLAG;
unsigned long ALARM_TIME;

unsigned long GPS_LAST, BT_TIME;


String dummy_lattitude = "3733.3614";
String dummy_longitude = "12702.7910";

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
  Serial3.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial3.available()) // 외부에서 노면 미끄러움 정보를 수신한 경우
  {
        char data = Serial3.read();
        BT_DATA += data;
        BT_FLAG =true;
        BT_TIME = millis();
  }
  else if(BT_FLAG == true && millis() - BT_TIME > 100)
  {
    BT_FLAG = false;
    if(BT_DATA == String("B\r\n"))
    {
      ALARM_FLAG = true;
      ALARM_TIME = millis();
      SEND_FLAG = true;
    }
    BT_DATA ="";

  }
  if(millis() - ALARM_TIME > 3000 && ALARM_FLAG == true)
  {
    ALARM_FLAG = false; //경보 해제
    SEND_FLAG = true;
  }
  //////////////////////////////////////////////////////////////////////////////////
  if(Serial.available())  // 자동차 내장 라즈베리파이가 노면 미끄러움을 영상으로 인식한 경우
  {
        char data = Serial.read();
        RASP_DATA += data;
        RASP_FLAG = true;
  }
  else if(RASP_FLAG == true)
  {
    RASP_FLAG = false;
    Serial3.println(RASP_DATA);
    RASP_DATA ="";
  }
  if( RASP_DATA == "B")
  {
    SEND_FLAG = true;
  }
  //////////////////////////////////////////////////////////////////////////////////
 
    
  
  if(GPS.available() && !Serial3.available() && !Serial.available())
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
  }



  if(SEND_FLAG == true)
  {
    if(lattitude.length() <3)
      lattitude = dummy_lattitude;
    if(longitude.length() <3)
      longitude = dummy_longitude;
    SEND_FLAG = false;
      Serial.print("A ,");
      Serial.print(lattitude); Serial.print(",");
      Serial.print(longitude); Serial.print(",");
      Serial.print(hum);       Serial.print(",");
      Serial.print(temp);      Serial.print(",");
      Serial.print(ALARM_FLAG ? 'T' : 'F');  Serial.print(",");
      Serial.println();
  }
}
