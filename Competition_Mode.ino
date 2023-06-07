/**
 * @file
 * This is the code for the competition mode as of 2/6/2023.
 */
#include <FastLED.h>

#define Voltage_In_Pin A0   // Pin to sense voltage transducer output
#define Current_In_Pin A2   // Pin to sense current transducer output
#define PWM_Pin 2           // Pin to do PWM switiching on the mosfet
#define LED_PIN 13           // Pin that controls the LED strip
#define NUM_LEDS 60         // Number of LEDs on the LED strip

CRGB leds[NUM_LEDS];        // Initialising the LED strip

// Pins for 3 way dial that controls the difficulty level
const int D_OUT[4] = {23, 25, 27, 29};  // Pins used to supply 5V to 3 way dial
const int D_READ[4] = {42, 38, 34, 30}; // Pins used to read the state of the 3 way dial

bool state[4] = {0,0,0,0};  // variable to store the states of eacher 3 way dial pin 

float pwm_period  = 200;    // length of time in pwm period
float duty_cycle  = 1;      // variable to hold selected duty cycle for switching
int duration  = 5;          // length of time to sample voltage and current 
float total_v;              // variable to store the running total for voltage for the duty cycle
float total_c;              // variable to store the running total for current for the duty cycle
float cum_energy = 0;       // cumulative energy total
float frequency;            
unsigned long starttime;    // time variable to start sampling voltage and current
float avg_current;    
float avg_voltage;
float inst_power;   
float max_voltage = 0;      // to put on the led strip at the end
float energy;
int val;                    // to light led strip

/**
 * @brief Function to decide the duty cycle of the PWM switching using the 3-way dial.
 * @return The selected duty cycle.
 */
float difficulty(){

  state[0] = digitalRead(D_READ[0]);
  state[1] = digitalRead(D_READ[1]);
  state[2] = digitalRead(D_READ[2]);
  state[3] = digitalRead(D_READ[3]);

  if(state[0] == HIGH && state[3] == HIGH){
    return 0.3;
  }
  else if(state[1] == HIGH && state[2] == HIGH){
    return 1;
  }
  else{
    return 0.6;
  }
}

/**
 * @brief Function to sample the current.
 * @param duration The duration for sampling.
 * @return The average current.
 */
float SampleCurrent(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float transducer_ref = 2.5;
  float reference_voltage = 5;
  float primary_current = 0;
  float nominal_current = 15;
  float total = 0;
  float sample_time = 0.2;
  float samples = duration / sample_time;

  unsigned long starttime = millis();
  unsigned long endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Current_In_Pin);
    adc_voltage = adc_value * reference_voltage / 1023;
    primary_current = 24 * (adc_voltage - transducer_ref);
    total += primary_current; 
    delay(sample_time);
    endtime = millis();
  }

  float avg_current = (total / samples) / 1.666;
  return avg_current;
}

/**
 * @brief Function to sample the voltage.
 * @param duration The duration for sampling.
 * @return The average voltage.
 */
float SampleVoltage(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float reference_voltage = 5;
  float voltage_max = 150.5;
  float total = 0;
  float sampling_time = 0.2;
  float samples = duration / sampling_time;

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Voltage_In_Pin); // between 0 and 1023
    float voltage_in = adc_value * voltage_max / 1023.0; // voltage value between 0 and 150.5 V
    total = total + voltage_in;
    delay(sampling_time);
    endtime = millis();
  }

  float avg_voltage =  total / samples;
  return avg_voltage;
}

/**
 * @brief Function to perform the switching cycle.
 * @param runtime The duration of the switching cycle.
 * @param duty The duty cycle for switching.
 */
void cycle(int runtime, float duty){

  //Serial.println("0,0,0,0,0");
  unsigned long stime = millis();
  float t_on = duty * pwm_period;
  float t_off = pwm_period - t_on;
  

  while((millis() - stime) <= runtime){
    digitalWrite(PWM_Pin, HIGH);
    FastLED.clear();
    total_v = 0; // variable to store the running total for voltage for the duty cycle
    total_c = 0; //

    starttime = millis();

    while((millis() - starttime) <= t_on){ // sample current and voltage whilst duty cycle is high
      total_c += SampleCurrent(duration);
      total_v += SampleVoltage(duration);
      // this loop takes 10ms
    }


    avg_current = duty_cycle * (total_c / (t_on/(duration * 2)));

    avg_voltage = 1.8 * duty_cycle * (total_v / (t_on/(duration * 2)));

    if(avg_voltage < 10){
      avg_voltage = 0;
      avg_current = 0;
    }


    if(avg_voltage > max_voltage){
      max_voltage = avg_voltage;
    }

    // frequency values based on mapping voltage to frequency tests that took place for different duty cycles
    if(duty == 0.3){
      frequency = 1.13 * avg_voltage + 3.1;
    }
    else if(duty == 0.6){
      frequency = 1.27 * avg_voltage - 1.19;
    }
    else if(duty == 1){
      frequency = 1.26 * avg_voltage + 0.25;
    }

    if(avg_current < 0){
      avg_current = -avg_current;
    }

    inst_power = avg_current * avg_voltage;

    energy = inst_power * ((float)pwm_period/1000);

    cum_energy = cum_energy + energy;

    val = map(avg_voltage, 0, 100, 0, NUM_LEDS); // here voltage is being mapped to the LED strip not power
    for(int i = 0; i < val; i++){
      leds[i] = CRGB::Red;
      FastLED.show();
    }

    Serial.print(avg_current, 2); Serial.print(","); Serial.print(avg_voltage, 2); Serial.print(","); Serial.print(inst_power, 2);
    Serial.print(","); Serial.print(cum_energy, 2); Serial.print(","); Serial.print(frequency, 1); /*Serial.print(","); Serial.print(remaining, 1)*/;
    Serial.println("");
    digitalWrite(PWM_Pin, LOW);
    delay(t_off);
  }
}
void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  pinMode(PWM_Pin, OUTPUT);
  digitalWrite(PWM_Pin, HIGH);
  for(int i = 0; i < 4; i++){
    pinMode(D_READ[i], INPUT_PULLUP);
    pinMode(D_OUT[i], OUTPUT);
  }

  duty_cycle = difficulty();

  Serial.begin(9600);
  //analogReference(EXTERNAL);
  //delay(800);
  cycle(10000, duty_cycle);
  digitalWrite(PWM_Pin, HIGH);
  val = map(max_voltage, 0, 150, 0, NUM_LEDS); // here voltage is being mapped to the LED strip not power
  for(int i = 0; i < val; i++){
    leds[i] = CRGB::Red;
    FastLED.show();
  }
  Serial.println("Done");

}

void loop() {
}
