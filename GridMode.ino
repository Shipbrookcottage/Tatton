/**
 * @file
 * This is the code for the competition mode as of 7/6/2023.
 */

/**
 * @brief Digital pins for interactive loads pushbutton.
 */
const int pushButton[3] = {5, 4, 3};
/**
 * @brief Pushbutton for the Emergency Stop button.
 */
const int pushButton_ES = 6;

/**
 * @brief Digital pins for solid state relay channels.
 */
const int SSRPin[3] = {8, 9, 10};

/**
 * @brief Digital Pins for emergency stop SSR.
 */
const int SSR_ES = 11;

/**
 * @brief Checks current status of the pushbutton for interactive loads and emergency stop.
 */
int pushbuttonState[3] = {0, 0, 0};
/**
 * @brief Checks current status of the emergency stop pushbutton.
 */
int pushbuttonState_ES = 1;

/**
 * @brief Stores current status of the SSR.
 */
int SSRStatus[3] = {HIGH, HIGH, HIGH};

/**
 * @brief Stores current status of the emergency stop SSR.
 */
int SSR_Status_ES = HIGH;

/**
 * @brief Stores current status of the Pushbuttons for renewables.
 */
int PushbuttonStatus = HIGH;

/**
 * @brief High trigger signal to turn SSR on.
 */
int SSRON = HIGH;

/**
 * @brief Low trigger signal to turn SSR off.
 */
int SSROFF = LOW;

/**
 * @brief Checks if the solar panel is switched on.
 */
int solar_state = 0;

/**
 * @brief Checks if the wind turbine is switched on.
 */
int wind_state = 0;

/**
 * @brief Pin for the MOSFET.
 */
const int MOSFET = 2;
/**
 * @brief Defines pin for hall sensor.
 */
#define Digital_In_Pin 18

/**
 * @brief Hall sensor value.
 */
int hall_sensor = 0;

/**
 * @brief Previous time value for frequency measurement.
 */
unsigned long t1 = 0;

/**
 * @brief New time value for frequency measurement.
 */
unsigned long t2 = 0;

/**
 * @brief Duty cycle for PWM.
 */
float duty_cycle = 0;

/**
 * @brief Frequency value.
 */
float frequency = 0;

/**
 * @brief Flag for calculating frequency.
 */
bool freq_flag = LOW;

/**
 * @brief Previous frequency value.
 */
float old_freq = 0;

/**
 * @brief Total load value.
 */
int load = 0;

/**
 * @brief PWM time period.
 */
const int time_period = 200;
/**
 * @brief Load values for different components.
 */
const int FIVEWATT_Led = 2;
const int SEVENWATT_Motor = 3;
const int FOURTYWATT_Bulb = 5;
const int solar = 4;
const int wind = 4;

/**
 * @brief Start time for frequency monitoring.
 */
unsigned long timerStart = 0;

/**
 * @brief Delay for frequency monitoring.
 */
const unsigned long timerDelay = 5000;
/**
 * @brief Flag to track if loads need to be powered off.
 */
bool loadPowerOff = false;

/**
 * @brief Flag to indicate if the system has started.
 */
bool startFlag = false;

/**
 * @brief Timer flag for frequency monitoring.
 */
int timerFlag = 0;

/**
 * @brief Setup function called once at the start.
 */
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

/**
 * @brief Main loop function.
 */
void loop() {
  bool solar_flag = LOW;
  bool wind_flag = LOW;
  load = 0;
  float solar_voltage = analogRead(A4)*5*5.0/1023;     //PV panel voltage
  if(solar_voltage > 13) {
    solar_state = 1;
  }
  else{
    solar_state = 0;
  }
  float wind_voltage = analogRead(A6)*5*5.0/1023;
  if(wind_voltage > 0.2) {
    wind_state = 1;
  }
  else {
    wind_state = 0;
  }
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
  
    if(pushbuttonState[0] == HIGH) {
      load = load + FIVEWATT_Led; // 5 w bulb added to load variable
    }
    if(pushbuttonState[1] == HIGH) {
      load = load + SEVENWATT_Motor; // 7 w motor added to load variable
    }
    if(pushbuttonState[2] == HIGH) {
      load = load + FOURTYWATT_Bulb; // 40 w bulb added to load variable
    }
    if(solar_state == HIGH) {
      load = load - solar;
      solar_flag = HIGH;
    }
    if(wind_state == HIGH) {
      load = load - wind;
      wind_flag = HIGH;
    }
  // PWM code
if (load >= 0){
  duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(MOSFET,  HIGH);
    delay(t_on);
    digitalWrite(MOSFET, LOW);
    delay(t_off);
  }
else{
  if(solar_flag == HIGH) {
    load = load + solar;
  }
  if(wind_flag == HIGH) {
    load = load + wind;
  }
  duty_cycle = float(load)/10;
  float t_on= duty_cycle * time_period;
  float t_off= (1- (duty_cycle)) * time_period;
    digitalWrite(MOSFET,  LOW);
    delay(time_period);
  }
  checkSpeed(old_freq);
  Serial.print(old_freq, 0); Serial.print(","); Serial.print(wind_voltage, 1); Serial.print(","); Serial.print(solar_voltage, 1); Serial.println("");
}

/**
 * @brief Calculate frequency based on time intervals.
 *
 * @param t1 The previous time value.
 * @param t2 The new time value.
 */
void freq(unsigned long t1, unsigned long t2){
  float frequency = ((1000/((float)t2-(float)t1))/2)*6; //milliseconds
  if(frequency > 1.3*old_freq && frequency>60) {        // This line is to try and prevent the speed meter from flickering around
    frequency = old_freq;
  }
  old_freq = frequency;
  if(frequency >= 35 && frequency <= 65){
    startFlag = true;
    timerFlag = timerFlag + 1;
  }
}

/**
 * @brief Check the speed and control the load power accordingly.
 *
 * @param frequency The current frequency value.
 */
void checkSpeed(float frequency){

  if(timerFlag == 1){
    timerStart = millis();
  }

  if (startFlag == true && (frequency < 45 || frequency > 55) && (millis() - timerStart >= timerDelay)) {
    loadPowerOff = true;
  }

  // Power off the interactive loads
  if (loadPowerOff) {
    TurnOff();
    loadPowerOff = false; // Reset the flag
  }
  if (frequency >= 45 && frequency <= 55) {
    timerStart = millis(); // Reset the timer start time
  }
}

/**
 * @brief Turn off all the loads.
 */
void TurnOff(){
  Serial.println("DONE");
  for (int i = 0; i < 3; i++) {
      digitalWrite(SSRPin[i], SSROFF);
    }
    digitalWrite(SSR_ES, SSROFF);
  while(1){

  }
}

/**
 * @brief Interrupt service routine for frequency measurement.
 */
void frequency_func() {
  if(freq_flag == LOW){
    t1 = millis();
    freq_flag = HIGH;
  }
  else{
    t2 = millis();
    freq(t1, t2);
    freq_flag = LOW;
  }
}
