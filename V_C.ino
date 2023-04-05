// This is code the will sense ac current and voltage around a PWM period of 200ms
// with LED strip integrated
#include <FastLED.h>

#define Current_In_Pin A5
#define Voltage_In_Pin A1
#define PWM_Pin 2
#define LED_PIN 8
#define NUM_LEDS 60
CRGB leds[NUM_LEDS];

int sampling_period  = 200;
float duty_cycle  = 0.5;
int duration  = 5;
float t_on = duty_cycle * sampling_period;
float t_off = sampling_period - t_on;

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

  Serial.println("Start");

}

void loop() {
  // put your main code here, to run repeatedly:
  FastLED.clear();
  float total_v = 0; // variable to store the running total for voltage for the duty cycle
  float total_c = 0; //
  digitalWrite(PWM_Pin, HIGH);

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= t_on){ // sample current and voltage whilst duty cycle is high
    total_c += SampleCurrent(duration);
    total_v += SampleVoltage(duration);
    endtime = millis();
    // this loop takes 10ms
  }

  digitalWrite(PWM_Pin, LOW);

  float avg_voltage = duty_cycle * (total_v / (t_on/(duration * 2)));

  Serial.print("V");
  Serial.println(avg_voltage, 5); // send voltage to python averaged over the 200 ms period

  int val = map(avg_voltage, 0, 150, 0, NUM_LEDS);

  for(int i = 0; i < val; i++){

    leds[i] = CRGB::Blue;
    FastLED.show();

  }

  float avg_current = duty_cycle * (total_c / (t_on/(duration * 2)));
  Serial.print("C");
  Serial.println(avg_current, 5);

  float inst_power = avg_current * avg_voltage;
  Serial.print("P");
  Serial.println(inst_power, 5);

}
