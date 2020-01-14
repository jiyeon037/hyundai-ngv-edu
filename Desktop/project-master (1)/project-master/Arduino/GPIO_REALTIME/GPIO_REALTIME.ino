void setup() {
  pinMode(13,OUTPUT);
  pinMode(2,INPUT_PULLUP);
  pinMode(3,INPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println(digitalRead(3));
  if(digitalRead(2)==LOW){
    if(millis()%1000>500)
    digitalWrite(13,HIGH);
    else
    digitalWrite(13,LOW);
  }
  else
  digitalWrite(13,LOW);
}
