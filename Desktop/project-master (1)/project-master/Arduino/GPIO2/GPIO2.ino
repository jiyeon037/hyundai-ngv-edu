#include <Servo.h>
int flag = false;
int angle;
int FACTOR = 0;
boolean angle_direction= false;
Servo mysv;
void setup() {
  // put your setup code here, to run once:
  mysv.attach(9);
  mysv.write(0); 
  pinMode(8,INPUT_PULLUP);
  pinMode(13,OUTPUT);
}

void loop()
{
  if(digitalRead(8) == LOW)
  {
     digitalWrite(13,HIGH);
     if(angle >= 180){ angle_direction = true;  }
     if(angle <0    ){ angle_direction = false; }
     if(angle_direction == false)
     {
        FACTOR = 1; // 각도 증가 모드
     }
     else
     {
        FACTOR = -1; // 각도 감소 모드
     }
     if(millis() % 30 < 15 && flag == true)
     {
      flag = false;
      angle = angle + FACTOR;
      mysv.write(angle);
     }
     if(millis() % 30 > 15)
     {
      flag = true;
     }
  }
  else
  {
    digitalWrite(13,LOW);
     if(millis() % 30 < 15 && flag == true)
     {
      flag = false;
      if(angle > 0)
        angle = angle -1;
      mysv.write(angle);
     }
     if(millis() % 30 > 15)
     {
      flag = true;
     }
  }
}
