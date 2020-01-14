/*  20191230 3조 아두이노 과제
  사용 센서 : 초음파센서
  사용 출력 : LCD 및 D13 GPIO
  일정 거리 이하로 물체가 감지되면 D13의 상태 toggle 주기 변경
  실시간 감지된 거리 LCD 화면 출력
  //LiquidCrystal(RS, E, D4, D5, D6, D7): LCD 라이브러리 초기화 함수
  //LiquidCrystal lcd(12, 11, 4, 5, 6, 7);
  //RS: LCD의 저장 공간에 값을 넣을 때 사용
  //E: LCD에 값을 쓸 수 있도록 할지 설정
  //Dn: LCD와 아두이노 사이의 입출력 핀
*/

#include LiquidCrystal lcd(12, 11, 4, 5, 6, 7); 
int trig = A1;//초음파 송신 2번 핀에 연결 
int echo = A2;//초음파 수신 3번 핀에 연결 
double duration;
double distance;

void setup() {
  pinMode(A0, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(A0, HIGH);
  pinMode(trig, OUTPUT);//trig 핀을 출력핀으로
  pinMode(echo, INPUT);//echo 핀을 입력핀으로
  Serial.begin(9600);//시리얼 통신을 위하여 통신 포트 열기
  lcd.begin(16, 2);
  lcd.print("Hello, world!");
}

void loop()
{
  digitalWrite(trig, HIGH);
  delay(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH, 20000);//pulseIn함수의 단위는 us(마이크로 세컨드)
  distance = (34 * ((double)1 / 1000)*duration) / 2;
  Serial.print(distance);
  Serial.println("cm");
  lcd.home();
  lcd.print("DISTANCE : ");
  lcd.print(distance);
  lcd.setCursor(0, 1);
  distance = (int)distance;

  if (distance > 40) {
    lcd.print(" VERY FAR       ");

    if (millis() % 2000 < 1000)
      digitalWrite(13, HIGH);
    else
      digitalWrite(13, LOW);
  }

  if (distance > 20 && distance < 40) {
    lcd.print(" FAR            ");
    if (millis() % 1000 < 500)
      digitalWrite(13, HIGH);
    else
      digitalWrite(13, LOW);
  }

  if (distance > 4 && distance < 20) {
    lcd.print(" NEAR            ");
    if (millis() % 200 < 100)
      digitalWrite(13, HIGH);
    else
      digitalWrite(13, LOW);
  }
}
