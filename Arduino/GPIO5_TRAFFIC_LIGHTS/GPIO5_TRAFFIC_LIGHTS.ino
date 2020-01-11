/* 
*  
  * 1. 신호등 작성(45분)  
   - 차량용 직진, 정지준비, 정지  
   - 보행자용 신호  
 2. 보행자용 신호등 점멸 기능 추가(30분)  
   - 보행자용 신호등 유지시간 30초  
   - 유지시간 중 마지막 10초에서는 보행자 직진 신호 등 점멸  
 3. 보행자용 호출 단추 기능 추가(30분)  
   - 호출 후 5초 뒤에 보행자 신호등 직진으로 변경 
*/ 

boolean human_button,human_button2; 
unsigned long human_time, normal_time; 
void setup() { 
 pinMode(11,OUTPUT); pinMode(10,OUTPUT); pinMode(9,OUTPUT);  
 pinMode(8,OUTPUT); digitalWrite(8,LOW); 
 pinMode(6,OUTPUT); pinMode(5,OUTPUT); pinMode(4,OUTPUT); 
 pinMode(3,OUTPUT); digitalWrite(3,LOW); 
 pinMode(2,INPUT_PULLUP); 
 normal_time = millis(); 
} 

void DELAY_FUCTION() 
{ 
     digitalWrite(10,HIGH); // 보행자 red 
     digitalWrite(11,LOW); // 보행자 blue 
     digitalWrite(6,LOW); // 자동차 blue 
     digitalWrite(5,HIGH); // 자동차 RED 
     digitalWrite(4,HIGH); // 자동차 green 
     delay(5000); 
     digitalWrite(10,LOW); // 보행자 red 
     digitalWrite(11,HIGH); // 보행자 blue 
     digitalWrite(6,LOW); // 자동차 blue 
     digitalWrite(5,HIGH); // 자동차 RED 
     digitalWrite(4,LOW); // 자동차 green 
} 
void loop() { 
  
 // put your main code here, to run repeatedly: 
 if(digitalRead(2) == LOW && digitalRead(11) == HIGH) 
 { 
   human_time = millis(); 
   human_button = true; 
 } // 사용자가 버튼을 누르기까지 기다리는 부분 
 if(millis() - human_time > 5000 && human_button == true) 
 { 
   DELAY_FUCTION(); 
   human_button2 = true; 
 } // 사용자가 버튼을 누르고 5초 지나야 보행자 시퀸스 루프에 들어감 

 // 보행자 시퀸스 루프 
 if(human_button2== true) // 사용자가 버튼을 누른 경우 
 { 
   while(1)  
   { 
     if(millis() - human_time <  24000) 
     { 
       digitalWrite(5,HIGH); // 자동차 RED 
       digitalWrite(11,HIGH); // 보행자 blue 
     } 
     else if(millis() - human_time < 34000 ) 
     { 
       digitalWrite(5,HIGH); // 자동차 RED 
       if(millis() % 3000 < 1500) digitalWrite(11,HIGH); 
       else  digitalWrite(11,LOW); 
     } 
     if(millis() - human_time >= 34000 ) 
     { 
       digitalWrite(5,LOW); // 자동차 RED 
       digitalWrite(11,LOW); // 보행자 BLUE 
       human_button2 = false; // 무한 시퀸스 탈출을 위한 flag 변화 
       human_button = false; 
       normal_time = millis(); 
       break; 
     } 
   } 
 } 
 /////// 평상시 상태 
   if((millis()-normal_time) % 10000 < 3000) 
   { 
     digitalWrite(10,HIGH); // 보행자 red 
     digitalWrite(11,LOW); // 보행자 blue 
     digitalWrite(6,HIGH); // 자동차 blue 
     digitalWrite(5,LOW); // 자동차 RED 
     digitalWrite(4,LOW); // 자동차 green       
   } 
   else if((millis()-normal_time) %10000 < 6000) 
   { 
     digitalWrite(10,HIGH); // 보행자 red 
     digitalWrite(11,LOW); // 보행자 blue 
      
     digitalWrite(6,LOW); // 자동차 blue 
     digitalWrite(5,HIGH); // 자동차 RED 
     digitalWrite(4,HIGH); // 자동차 green 
   } 
   else if((millis()-normal_time) %10000 < 9000) 
   { 
     digitalWrite(10,LOW); // 보행자 red 
     digitalWrite(11,HIGH); // 보행자 blue 
     digitalWrite(6,LOW); // 자동차 blue 
     digitalWrite(5,HIGH); // 자동차 RED 
     digitalWrite(4,LOW); // 자동차 green 
   } 
   else 
   { 
     normal_time = millis(); 
   } 
  
}
