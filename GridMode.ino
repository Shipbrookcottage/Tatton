const int pushButton[3] = {3,4,5}; // digital pins for interactive loads and emergency stop
const int pushButton_ES = 6;
const int pushButton_Renewables = 7; // didgtal pins for renewables push button
const int SSRPin[3] = {8,9,10}; // digital pins for solid state relay channels.
const int SSR_ES = 11;
int pushbuttonState[3] = {0,0,0}; //checks current status of the pushbutton for interactive loads and emergency stop
int pushbuttonState_ES = 1;
int pushbuttonState_renewables = 0;
int SSRStatus[3] = {HIGH,HIGH,HIGH}; // stores current status of the SSR
int SSR_Status_ES = HIGH;
int PushbuttonStatus = HIGH;// stores current status of the Pushbuttons for renewables
int SSRON = HIGH; //high trigger signal to turn SSR on
int SSROFF = LOW; // low trigger signal to turn SSR off
int solar_state = 0; // checks if the the solar panel is switched on
int wind_state = 0; // checks if the wind turbine is switched on
const int MOSFET = 2;
#define Digital_In_Pin 18 //defines pin for hall sensor
int hall_sensor = 0;
unsigned long t1 = 0; // previous time value
unsigned long t2 = 0; // new time value
float frequency = 0;
bool flag = LOW;

float old_freq = 0;
int load = 0;
const int time_period = 200; // PWM time period
const int FIVEWATT_Led = 2;
const int SEVENWATT_Motor = 3;
const int FOURTYWATT_Bulb = 5;
const int solar = 3;
const int wind = 3;
unsigned long timerStart = 0; // start time for frequency monitoring
const unsigned long timerDelay = 5000; // 5-second delay for frequency monitoring
bool loadPowerOff = false; // flag to track if loads need to be powered off
bool startFlag = false;
int timerFlag = 0;


void setup() {
  Serial.begin(9600);
  for(int i=0;i<3;i++) {
    pinMode(pushButton[i],INPUT_PULLUP); // configures pushbutton for enable the state of the push button to be read
    pinMode(SSRPin[i],OUTPUT); // sets SSR to output mode
    digitalWrite(SSRPin[i], SSROFF); // sets initial status of the relay as OFF
  }
  pinMode(pushButton_ES,INPUT_PULLUP); // configures pushbutton for enable the state of the push button to be read
  pinMode(SSR_ES,OUTPUT); // sets SSR to output mode
  digitalWrite(SSR_ES, SSROFF); // sets initial status of the relay as OFF

  pinMode(MOSFET, OUTPUT);
  digitalWrite(MOSFET, LOW);
  attachInterrupt(digitalPinToInterrupt(Digital_In_Pin),frequency_func,FALLING); // attaches interrupt for Hall sensor pin
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
  float wind_voltage = analogRead(A6)*5*5.0/1023;
  if(wind_voltage > 0.4) {
    wind_state = 1;
  }
  else {
    wind_state = 0;
  }
  //Serial.println(solar_voltage);  
  //Serial.println(wind_voltage);
  int state_ES = 0;
  int state[3] = {0,0,0}; // initialises the current state of the interactive and emergency stop pushbuttons to zero
  int state_renewables = 0;

  state_ES = digitalRead(pushButton_ES);
  if (state_ES == HIGH && SSR_Status_ES == LOW){
    pushbuttonState_ES = !pushbuttonState_ES;
  }
  SSR_Status_ES = state_ES;
  if(pushbuttonState_ES == HIGH){
    digitalWrite(SSR_ES, SSRON); 
  } else {
    digitalWrite(SSR_ES, SSROFF); 
  }

    for(int i=0;i<3;i++) {
      state[i] = digitalRead(pushButton[i]);
      if(state[i] == HIGH && SSRStatus[i] == LOW && startFlag == true) {
        pushbuttonState[i] = !pushbuttonState[i];
        delay(300);
      }
      SSRStatus[i] = state[i];
      if (pushbuttonState[i] == HIGH && startFlag == true) {
        digitalWrite(SSRPin[i], SSRON);
      } else {
        digitalWrite(SSRPin[i], SSROFF);
      }
    }
    state_renewables = digitalRead(pushButton_Renewables);
    if(state_renewables == HIGH && pushbuttonState_renewables == LOW) {
        pushbuttonState_renewables = !pushbuttonState_renewables;
      }
      pushbuttonState_renewables = state_renewables;
  
    if(pushbuttonState[0] == HIGH) {
      load = load + FIVEWATT_Led; // 5 w bulb added to load variable
    }
    if(pushbuttonState[1] == HIGH) {
      load = load + SEVENWATT_Motor; // 7 w motor added to load variable
    }
    if(pushbuttonState[2] == HIGH) {
      load = load + FOURTYWATT_Bulb; // 40 w bulb added to load variable
    }
    if(pushbuttonState_renewables == HIGH && solar_state == HIGH) {
      load = load - solar;
      solar_flag = HIGH;
    }
    if(pushbuttonState_renewables == HIGH && wind_state == HIGH) {
      load = load - wind;
      wind_flag = HIGH;
    }
  // PWM code
if (load >= 0){
  float duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(MOSFET,  HIGH);
    delay(t_on);
    digitalWrite(MOSFET, LOW);
    delay(t_off);
    //Serial.println(duty_cycle);
  }
else{
  if(solar_flag == HIGH) {
    load = load + solar;
  }
  if(wind_flag == HIGH) {
    load = load + wind;
  }
  float duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(MOSFET,  LOW);
    delay(time_period);
    //Serial.println(duty_cycle);
  }
  checkSpeed(old_freq);
}

void freq(unsigned long t1, unsigned long t2){
  float frequency = ((1000/((float)t2-(float)t1))/2)*6; //milliseconds
  if(frequency > 1.5*old_freq && frequency>60) {
    frequency = old_freq;
  }
  old_freq = frequency;
  Serial.println(frequency);
  if(frequency >= 45 && frequency <= 55){
    startFlag = true;
    timerFlag = timerFlag + 1;
  }
}

void checkSpeed(float frequency){

  if(timerFlag == 1){
    timerStart = millis();
  }

  if (startFlag == true && (frequency < 45 || frequency > 55) && (millis() - timerStart >= timerDelay)) {
    loadPowerOff = true;
  }

  // Power off the interactive loads
  if (loadPowerOff) {
    /*for (int i = 0; i < 4; i++) {
      digitalWrite(SSRPin[i], SSROFF);
    }*/
    TurnOff();
    loadPowerOff = false; // Reset the flag
  }
  if (frequency >= 45 && frequency <= 55) {
    timerStart = millis(); // Reset the timer start time
  }
}

void TurnOff(){
  Serial.println("DONE");
  for (int i = 0; i < 3; i++) {
      digitalWrite(SSRPin[i], SSROFF);
    }
    digitalWrite(SSR_ES, SSROFF);
  while(1){

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
  }
}
