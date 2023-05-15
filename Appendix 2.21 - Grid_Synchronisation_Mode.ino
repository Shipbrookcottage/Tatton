const int pushButton[4]= {10,12,13}; // digital pins for interactive loads and emergency stop 
const int pushButton_Renewables[2]= {24,25}; // didgtal pins for renewables push button
const int led[4] = {2,3,4,5};// digital pins for LED indicators for interactive loads and emergency stop 
const int led_renewables[2] = {22,29}; // digital pins for led indicators for renewables 
const int SSRPin[4] = {32,33,34,55}; // digital pins for solid state relay channels. 
int pushbuttonState[4] = {0,0,0,0}; //checks current status of the pushbutton for interactive loads and emergency stop 
int pushbuttonState_renewables[2] = {0,0};
int SSRStatus[4] = {HIGH,HIGH,HIGH,HIGH}; // stores current status of the SSR 
int PushbuttonStatus[2] = {HIGH,HIGH};// stores current status of the Pushbuttons for renewables 
int SSRON = HIGH; //high trigger signal to turn SSR on 
int SSROFF = LOW; // low trigger signal to turn SSR off 
int solar_state = 0; // checks if the the solar panel is switched on
int wind_state = 0; // checks if the wind turbine is switched on 
const int MOSFET = 53;
#define Digital_In_Pin 54 //defines pin for hall sensor 
int hall_sensor = 0;
unsigned long t1 = 0; // previous time value
unsigned long t2 = 0; // new time value
float frequency = 0;
bool flag = LOW;
const int Led_Hall_Sensor[3] = {26,27,28};

int load = 0;
const int time_period = 200; // PWM time period 
const int FIVEWATT_Led = 2;
const int SEVENWATT_Motor = 3;
const int FOURTYWATT_Bulb = 5; 
const int solar = 3;
const int wind = 3;
void setup() {
  Serial.begin(9600);
  for(int i=0;i<4;i++) {
    pinMode(pushButton[i],INPUT_PULLUP); // configures pushbutton for enable the state of the push button to be read
    pinMode(SSRPin[i],OUTPUT); // sets SSR to output mode 
    pinMode(led[i],OUTPUT); // sets LEDs to output mode
    digitalWrite(SSRPin[i], SSROFF); // sets initial status of the relay as OFF 
  }
  for(int i=0;i<2;i++) {
    pinMode(pushButton_Renewables[i],INPUT_PULLUP); // configures pushbutton for renewables
    pinMode(led_renewables[i],OUTPUT); // sets LEDs to output
  }  
  pinMode(MOSFET, OUTPUT); 
  digitalWrite(MOSFET, LOW);
  attachInterrupt(digitalPinToInterrupt(Digital_In_Pin),frequency_func,FALLING); // attaches interrupt for Hall sensor pin 
  for(int i=0;i<2;i++) {
    pinMode(Led_Hall_Sensor[i],OUTPUT); // sets LEDs to output
  }  
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
  Serial.println(solar_voltage);   
  Serial.println(wind_voltage);
  int state[4] = {0,0,0,0}; // initialises the current state of the interactive and emergency stop pushbuttons to zero 
  int state_renewables[2] = {0,0}; // initialises  the current state of the renewables push button to zero
  for(int i=0;i<4;i++) {
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
      digitalWrite(led[i],LOW);
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
  if(pushbuttonState_renewables[0] == HIGH && solar_state == HIGH) {
    load = load - solar;
    solar_flag = HIGH;
  }
  if(pushbuttonState_renewables[1] ==HIGH && wind_state == HIGH) {
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
void freq(unsigned long t1, unsigned long t2){ // function to calculate the frequecy and turn LEDs on depending on the current frequency 
  float frequency = 1000/((float)t2-(float)t1); //milliseconds
  Serial.println(frequency);
  if(frequency < 4) {
    digitalWrite(Led[0],HIGH);
  }
  else {
    digitalWrite(Led_Hall_Sensor[0],LOW);
  }
  if(frequency > 4 && frequency < 10) {
    digitalWrite(Led_Hall_Sensor[1],HIGH);
  }
  else {
    digitalWrite(Led_Hall_Sensor[1],LOW);
  }
  if(frequency > 10){
    digitalWrite(Led_Hall_Sensor[2],HIGH);
  }
  else {
    digitalWrite(Led_Hall_Sensor[2],LOW);
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

 

