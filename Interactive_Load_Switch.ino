const int pushButton[3]= {8,9,10};
const int pushButton_Renewables[2]= {24,25};
const int led[3] = {5,6,7};
const int led_renewables[2] = {22,23};
const int SSRPin[3] = {2,3,4};
int pushbuttonState[3] = {0,0,0};
int pushbuttonState_renewables[2] = {0,0};
int SSRStatus[3] = {HIGH,HIGH,HIGH};
int PushbuttonStatus[2] = {HIGH,HIGH};
int triggerType = HIGH; // HIGH trigger SSR is being used
int SSRON = HIGH;
int SSROFF = LOW;
int solar_state = 0;
int wind_state = 0;

void setup() {
  Serial.begin(9600);
  for(int i=0;i<3;i++) {
    pinMode(pushButton[i],INPUT_PULLUP); // configures pushbutton
    pinMode(SSRPin[i],OUTPUT); // sets SSR to output
    pinMode(led[i],OUTPUT); // sets LEDs to output
    digitalWrite(SSRPin[i], SSROFF); // sets initial status of the relay as OFF
  }
  for(int i=0;i<2;i++) {
    pinMode(pushButton_Renewables[i],INPUT_PULLUP); // configures pushbutton for renewables
    pinMode(led_renewables[i],OUTPUT); // sets LEDs to output
  }  
  pinMode(11, OUTPUT);
}
void loop() {
  float solar_voltage = analogRead(A0)*5*5.0/1023;     //PV panel voltage
  if(solar_voltage > 7) {
    solar_state = 1;
  }
  else{
    solar_state = 0;
  }
  float wind_voltage = (analogRead(A4)*(5/3))/1023;
  if(wind_voltage > 0.5) {
    wind_state = 1;
  }
  else {
    wind_state = 0;
  }
  Serial.println(solar_voltage);  
  int state[3] = {0,0,0}; // start at off state for pushbutton for loads
  int state_renewables[2] = {0,0}; // start at off state for pushbutton for renewables
  for(int i=0;i<3;i++) {
    state[i] = digitalRead(pushButton[i]);
    if(state[i] == HIGH && SSRStatus[i] == LOW) {
      pushbuttonState[i] = 1-pushbuttonState[i];
    }
    SSRStatus[i] = state[i];
    if (pushbuttonState[i] == HIGH) {
      //Serial.println ("SSR[i] ON");
      digitalWrite(led[i], HIGH);
      digitalWrite(SSRPin[i], SSRON);
    } else {
      //Serial.println ("SSR[i] OFF");
      digitalWrite(led[i], LOW);
      digitalWrite(SSRPin[i], SSROFF);
      //Serial.println("====");
    }
  }
  for(int i=0;i<2;i++) {
    state_renewables[i] = digitalRead(pushButton_Renewables[i]);
    if(state_renewables[i] == HIGH && PushbuttonStatus[i] == LOW) {
      pushbuttonState_renewables[i] = 1-pushbuttonState_renewables[i];
    }
    PushbuttonStatus[i] = state_renewables[i];
    if (pushbuttonState_renewables[i] == HIGH) {
      //Serial.println ("SSR[i] ON");
      digitalWrite(led_renewables[i], HIGH);
    } else {
      //Serial.println ("SSR[i] OFF");
      digitalWrite(led_renewables[i], LOW);
      //Serial.println("====");
    }
  }
    if((pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == HIGH && solar_state == HIGH && wind_state == HIGH)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == LOW && solar_state == HIGH && wind_state == LOW)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == HIGH))  
    {
      digitalWrite(11, HIGH);
      delay(120);
      digitalWrite(11,LOW);
      delay(80);
    }

    if(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == HIGH && solar_state == HIGH && wind_state == HIGH) {
      digitalWrite(11, HIGH);
      delay(200);
    }
    else if((pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == LOW)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == HIGH && solar_state == HIGH && wind_state == LOW)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == HIGH && solar_state == LOW && wind_state == HIGH))  
    {
      digitalWrite(11, HIGH);
      delay(160);
      digitalWrite(11, LOW);
      delay(40);
    }
    else if(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == HIGH && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, HIGH);
      delay(180);
      digitalWrite(11, LOW);
      delay(20);
    }
    else if((pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == HIGH && solar_state == HIGH && wind_state == LOW)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == HIGH && solar_state == LOW && wind_state == HIGH))  
    {
      digitalWrite(11, HIGH);
      delay(150);
      digitalWrite(11, LOW);
      delay(50);
    }
    else if((pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == HIGH && solar_state == HIGH && wind_state == HIGH)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == LOW && solar_state == HIGH && wind_state == LOW)||(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == HIGH))  
    {
      digitalWrite(11, HIGH);
      delay(110);
      digitalWrite(11, LOW);
      delay(90);
    }
    else if(pushbuttonState[0] == HIGH && pushbuttonState[1] == HIGH && pushbuttonState[2] == LOW && solar_state == HIGH && wind_state == HIGH) {
      digitalWrite(11, HIGH);
      delay(90);
      digitalWrite(11, LOW);
      delay(110); }
    else if(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == LOW && solar_state == HIGH && wind_state == HIGH) {
      digitalWrite(11, HIGH);
      delay(140);
      digitalWrite(11, LOW);
      delay(60);
      }
    else if(pushbuttonState[0] == HIGH && pushbuttonState[1] == LOW && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, HIGH);
      delay(140);
      digitalWrite(11, LOW);
      delay(60);
    }
    else if(pushbuttonState[0] == LOW && pushbuttonState[1] == HIGH && pushbuttonState[2] == HIGH && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, HIGH);
      delay(60);
      digitalWrite(11, LOW);
      delay(140);
    }
    else if(pushbuttonState[0] == LOW && pushbuttonState[1] == HIGH && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, HIGH);
      delay(20);
      digitalWrite(11, LOW);
      delay(180);
    }
    else if(pushbuttonState[0] == LOW && pushbuttonState[1] == LOW && pushbuttonState[2] == HIGH && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, HIGH);
      delay(40);
      digitalWrite(11, LOW);
      delay(160);
    }
    else if(pushbuttonState[0] == LOW && pushbuttonState[1] == LOW && pushbuttonState[2] == LOW && solar_state == LOW && wind_state == LOW) {
      digitalWrite(11, LOW);
    }

   
}
