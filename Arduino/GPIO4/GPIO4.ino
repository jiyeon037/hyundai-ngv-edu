  /* 20191230 과제 미션 7
  초음파 센서와 서보 모터를 이용한 서킷 만들기
  요구사항 :초음파 센서의 측정 거리에 따라서 서보 모터 각도가 변화 됨
  멀어질수록 각도가 크게 벌어지도록 함
  가변 저항을 부착하여 서보 모터의 변화 각도를 제한(최소 각도는 90도)
  */ 

// Set the LCD address to 0x27 for a 16 chars and 2 line display
#include LiquidCrystal_I2C lcd(0x3F, 16, 2);
#include Servo sv;

int trig = 5; 
int echo = 6;
double duration;
double distance;
int potential;
int DIRECT_FACTOR, angle_FACTOR;
int angle;

void setup()
{   pinMode(trig,OUTPUT);//trig 핀을 출력핀으로
  pinMode(echo,INPUT);//echo 핀을 입력핀으로
  Serial.begin(9600);//시리얼 통신을 위하여 통신 포트 열기
  lcd.begin();
  lcd.backlight();
  sv.attach(9);
  pinMode(A0,INPUT);
} 

void loop()
{ 
  // 초음파 센서를 이용해 거리 검출 시작
  digitalWrite(trig,HIGH);
  delay(10);
  digitalWrite(trig,LOW);
  duration = pulseIn(echo,HIGH,20000);//pulseIn함수의 단위는 us(마이크로 세컨드)
  distance = (34*((double)1/1000)*duration)/2;
  Serial.print(distance);
  Serial.println("cm"); // 초음파 센서를 이용해 거리 검출 시작
              
  // 화면 출력
  lcd.home();
  lcd.print("DISTANCE : ");
  lcd.print(distance);
  lcd.setCursor(0,1);
  distance = (int)distance; // 거리 감지 및 출력 시작
  angle_FACTOR = distance/ 10; // 초음파센서에서 감지된 거리를 10 cm로 나눈 값을 각도 증가 인자값으로 사용
  potential = analogRead(A0); // analogRead 를 통해 A0에 인가된 전압 읽어들임
  int angle_limit = map(potential,0,1023,90,180);
  lcd.setCursor(0,1);
  lcd.print("LIMIT ");
  lcd.print(angle_limit);
  lcd.print(" ");
  
  // 화면 출력 및 비례식 계산 끝 (map 함수 이용)
  // 방향전환부 시작
  if(angle > angle_limit)
    DIRECT_FACTOR = -1; // 각도 감소
  if(angle <= 0)
    DIRECT_FACTOR = 1; // 각도 증가
               // 방향전환부 끝
               // 서보모터 각도 제어 시작
  angle = angle + (DIRECT_FACTOR * angle_FACTOR);
  sv.write(angle); // 서보모터 각도 제어 끝
}
