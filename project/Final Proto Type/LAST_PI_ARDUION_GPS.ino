/*
 * 저자 : 노윤석 ( 123gtf@naver.com )
 * 날짜 : 2020/02/17
 * 
 * 자동차에 내장되는 디스플레이 장치 주변 아두이노에 업로드 되는 코드
 * 
 * 라즈베리파이 (센서 데이터 요청) -> 아두이노 (센서 데아터 처리) -> 라즈베리파이 
 * GPS 모듈을 통해 실시간 위도 및 경도 데이터 추출
 * DHT11 온습도 센서를 통해 실시간 대기 온습도 추출
 * 적외선 온도센서를 통한 실시간 노면 온도 추출 
 * HC-06을 통해 원격의 다른 차량에게 실시간 경고 신호 송신
 *  
 * 다른 자동차 -> 아두이노 -> 라즈베리파이
 * 주변 자동차에서 발생하는 경고 신호 수신해 라즈베리파이에 경고 신호 수신 내용 전달 
 * 
 */
#include <SoftwareSerial.h>
SoftwareSerial GPS(7,6);
#include<SPI.h>

#define OBJECT  0xA0      // 대상 온도 커맨드
#define SENSOR  0xA1      // 센서 온도 커맨드
boolean Timer1_Flag;
const int chipSelectPin  = 53;
int  iOBJECT, iSENSOR;  // 부호 2byte 온도 저장 변수 

String GPS_DATA;
String BT_DATA;
boolean BT_FLAG;
String RASP_DATA;
boolean RASP_FLAG;
boolean ALARM_FLAG,SEND_FLAG;
unsigned long ALARM_TIME;
unsigned long GPS_LAST, BT_TIME;

String dummy_lattitude = "3733.3614"; // 실내 GPS 안잡히는 경우, 임시 위도 경도
String dummy_longitude = "12702.7910"; 

#include "DHT.h"
#define DHTPIN 2  //온습도 센서 디지털 2번에 신호선 연결
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

      String lattitude;
      String longitude;
      int hum;
      int temp;
      float road_temp;

int SPI_COMMAND(unsigned char cCMD) // 적외선 온도 센서에 온도 정보 요청
{
    unsigned char T_high_byte, T_low_byte;
    digitalWrite(chipSelectPin , LOW);  
    delayMicroseconds(10);              
    SPI.transfer(cCMD);                
    delayMicroseconds(10);                     
    T_low_byte = SPI.transfer(0x22);   
    delayMicroseconds(10);               
    T_high_byte = SPI.transfer(0x22);  
    delayMicroseconds(10);             
    digitalWrite(chipSelectPin , HIGH);  
    return (T_high_byte<<8 | T_low_byte);  // 온도값 return 
}


void setup() {
  
  // put your setup code here, to run once:
  GPS.begin(9600);
  Serial.begin(9600);
  Serial3.begin(9600);
  digitalWrite(chipSelectPin , HIGH);    
  pinMode(chipSelectPin , OUTPUT);       
  SPI.setDataMode(SPI_MODE3);             
  SPI.setClockDivider(SPI_CLOCK_DIV16);  
  SPI.setBitOrder(MSBFIRST);                
  SPI.begin();                               
}

void loop()
{
  if(Serial3.available()) // 다른 차량에서 발생한 외부에서 노면 미끄러움 정보를 수신한 경우
  {
        char data = Serial3.read();
        BT_DATA += data;
        BT_FLAG =true;
        BT_TIME = millis();
  }
  else if(BT_FLAG == true && millis() - BT_TIME > 100)
  {
    BT_FLAG = false;
    Serial.println(BT_DATA.length());
    if(BT_DATA.indexOf('B') != -1)
    {
      Serial.println("hello");
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
    iOBJECT = SPI_COMMAND(OBJECT);      // 대상 온도 Read 
    road_temp = float(iOBJECT)/100,2;
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
      Serial.print(road_temp); Serial.print(",");
      Serial.print(ALARM_FLAG ? 'T' : 'F');  Serial.print(",");
      Serial.println();
  }
}
