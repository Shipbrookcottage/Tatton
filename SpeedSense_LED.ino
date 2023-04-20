#define Digital_In_Pin 2
int hall_sensor = 0;
unsigned long t1 = 0; // previous time value
unsigned long t2 = 0; // new time value
float frequency = 0;
bool flag = LOW;
const int Led[3] = {3,4,5};

void freq(unsigned long t1, unsigned long t2){
  float frequency = 1000/((float)t2-(float)t1); //milliseconds
  Serial.println(frequency);
  if(frequency < 4) {
    digitalWrite(Led[0],HIGH);
  }
  else {
    digitalWrite(Led[0],LOW);
  }
  if(frequency > 4 && frequency < 10) {
    digitalWrite(Led[1],HIGH);
  }
  else {
    digitalWrite(Led[1],LOW);
  }
  if(frequency > 10){
    digitalWrite(Led[2],HIGH);
  }
  else {
    digitalWrite(Led[2],LOW);
  }
}


void setup() {
  Serial.begin(9600);
  Serial.println("Frequency");
  attachInterrupt(digitalPinToInterrupt(Digital_In_Pin),frequency_func,FALLING);
  for(int i=0;i<2;i++) {
    pinMode(Led[i],OUTPUT); // sets LEDs to output
  }  
}
void frequency_func() {
  if(flag == LOW){
    t1 = millis();
    flag = HIGH;
  }
  else{
    t2 = millis();
    freq(t1, t2);
    flag = LOW;
   // Serial.println(t1);
    //Serial.println(t2);
  }
}

void loop() {
  hall_sensor = digitalRead(2);
  //Serial.println(hall_sensor);
  }
