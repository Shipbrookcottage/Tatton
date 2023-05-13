// This is the code for the competition mode as of 26/4/2023
#include <FastLED.h>

// Initialise pins 

#define Current_In_Pin A0
#define Voltage_In_Pin A1
#define PWM_Pin 2
#define LED_PIN 8
#define NUM_LEDS 60
CRGB leds[NUM_LEDS];

float sampling_period  = 200;
float duty_cycle  = 0.8;
int duration  = 5;
float t_on = duty_cycle * sampling_period;
float t_off = sampling_period - t_on;

float cum_energy = 0; // cumulative energy

float SampleCurrent(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float transducer_ref = 2.5;
  float reference_voltage = 5;
  float primary_current = 0;
  float nominal_current = 15;
  float total = 0;
  float sample_time = 0.1;
  float samples = duration / sample_time;

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Current_In_Pin);
    adc_voltage = adc_value * reference_voltage / 1024;
    primary_current = (nominal_current * (adc_voltage - transducer_ref)) / 0.625;
    total += primary_current; 
    delay(sample_time);
    endtime = millis();
  }

  float avg_current = total / samples;
  return avg_current;
}

float SampleVoltage(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float reference_voltage = 5;
  float voltage_max = 150.5;
  float total = 0;
  float sampling_time = 0.1;
  float samples = duration / sampling_time;

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Voltage_In_Pin); // between 0 and 1023
    float voltage_in = adc_value * voltage_max / 1024.0; // voltage value between 0 and 150.5 V
    total = total + voltage_in;
    delay(sampling_time);
    endtime = millis();
  }

  float avg_voltage = (2 * total) / samples;
  return avg_voltage;
}

void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  pinMode(PWM_Pin, OUTPUT);
  digitalWrite(PWM_Pin, HIGH);

  Serial.begin(9600);
  analogReference(EXTERNAL);

}

void loop() {
  // put your main code here, to run repeatedly:
  FastLED.clear();
  float total_v = 0; // variable to store the running total for voltage for the cycle
  float total_c = 0; // variable to store the running total for voltage for the cycle
  digitalWrite(PWM_Pin, HIGH); // set the MOSFET high

  float starttime = millis(); // Initialise timer
  float endtime = starttime;

  while((endtime - starttime) <= t_on){ // sample current and voltage whilst duty cycle is high
    total_c += SampleCurrent(duration); // Sample for 5ms
    total_v += SampleVoltage(duration);
    endtime = millis();
    // this loop takes 10ms
  }

  digitalWrite(PWM_Pin, LOW); // Set MOSFET low at the end of the on period.

  float avg_current = duty_cycle * (total_c / (t_on/(duration * 2))); // calculate average current based on duty cycle

  float avg_voltage = duty_cycle * (total_v / (t_on/(duration * 2))); // calculate average voltage based on duty cycle

  float inst_power = avg_current * avg_voltage; // calculate power produced in the total cycle period

  int val = map(avg_voltage, 0, 150, 0, NUM_LEDS); // here voltage is being mapped to the LED strip not power

  for(int i = 0; i < val; i++){

    leds[i] = CRGB::Blue;
    FastLED.show(); // Turn on the number of LEDs corresponding to the mapped voltage values

  }
  

  delay(t_off); // Keep the MOSFET low for t_off

  float energy = inst_power * ((float)sampling_period/1000);
  cum_energy = cum_energy + energy;
  Serial.print(avg_current, 2); Serial.print(","); Serial.print(avg_voltage, 2); Serial.print(","); Serial.print(inst_power, 2);
  Serial.print(","); Serial.print(cum_energy, 2); Serial.println(""); // send data to the PC using serial.print

}
