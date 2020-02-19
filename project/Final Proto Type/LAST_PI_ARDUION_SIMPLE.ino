/*
 * 저자 : 노윤석 ( 123gtf@naver.com )
 * 날짜 : 2020/02/17
 * 
 * 차량간 V2X 구현을 위한 모니터단에서 운용되는 아두이노 코드
 * 아두이노는 단순 Serial to USB TTL 변환기 역할을 하도록 제작
 * 통신속도 개선 코드
 */
#include <SoftwareSerial.h>
SoftwareSerial BT(8,9);
void setup() {
  // put your setup code here, to run once:
  BT.begin(9600);
  Serial.begin(9600);
  delay(1000);
  BT.write("C\n");
  Serial.write("C\n");
}

void loop()
{
  if(BT.available())
  { 
    char data = BT.read();
    Serial.write(data);
  }
  if(Serial.available())
  {
    char data = Serial.read();
    BT.write(data);
  }
}
