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

int load = 0;
const int time_period = 200;
const int FIVEWATT_Led = 2;
const int SEVENWATT_Motor = 3;
const int FOURTYWATT_Bulb = 5;
const int solar = 3;
const int wind = 3;
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
  digitalWrite(11, LOW);
}
void loop() {
  bool solar_flag = LOW;
  bool wind_flag = LOW;
  load = 0;
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
  //Serial.println(solar_voltage);  
  int state[3] = {0,0,0}; // start at off state for pushbutton for loads
  int state_renewables[2] = {0,0}; // start at off state for pushbutton for renewables
  for(int i=0;i<3;i++) {
    state[i] = digitalRead(pushButton[i]);
    if(state[i] == HIGH && SSRStatus[i] == LOW) {
      pushbuttonState[i] = 1-pushbuttonState[i];
    }
    SSRStatus[i] = state[i];
    if (pushbuttonState[i] == HIGH) {
      digitalWrite(led[i], HIGH);
      digitalWrite(SSRPin[i], SSRON);
    } else {
      digitalWrite(led[i], LOW);
      digitalWrite(SSRPin[i], SSROFF);
    }
  }
  for(int i=0;i<2;i++) {
    state_renewables[i] = digitalRead(pushButton_Renewables[i]);
    if(state_renewables[i] == HIGH && PushbuttonStatus[i] == LOW) {
      pushbuttonState_renewables[i] = 1-pushbuttonState_renewables[i];
    }
    PushbuttonStatus[i] = state_renewables[i];
    if (pushbuttonState_renewables[i] == HIGH) {
      digitalWrite(led_renewables[i], HIGH);
    }
    else {
      digitalWrite(led_renewables[i], LOW);
    }
  }
  if(pushbuttonState[0] == HIGH) {
    load = load + FIVEWATT_Led; // 5 w bulb added to load variable
  }
  if(pushbuttonState[1] == HIGH) {
    load = load + SEVENWATT_Motor; // 7 w motor added to load variable
  }
  if(pushbuttonState[2] == HIGH) {
    load = load + FOURTYWATT_Bulb; // 40 w bulb added to load variable
  }
  if(pushbuttonState_renewables[0] == HIGH) {
    load = load - solar;
    solar_flag = HIGH;
  }
  if(pushbuttonState_renewables[1] == HIGH) {
    load = load - wind;
    wind_flag = HIGH;
  }
  // PWM code
if (load >= 0){
  float duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(11,  HIGH);
    delay(t_on);
    digitalWrite(11, LOW);
    delay(t_off);
    Serial.println(duty_cycle);
  }
else{
  if(solar_flag == HIGH) {
    load = load + solar;
    digitalWrite(led_renewables[0],LOW);
  }
  if(wind_flag == HIGH) {
    load = load + wind;
    digitalWrite(led_renewables[1],LOW);
  }
  float duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(11,  LOW);
    delay(time_period);
    Serial.println(duty_cycle);
  }
}
