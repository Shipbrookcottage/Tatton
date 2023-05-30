// This is the code for the competition mode as of 28/5/2023
// This code will use the mapped frequency values to send frequency
#include <FastLED.h>

#define Current_In_Pin A5
#define Voltage_In_Pin A0
#define PWM_Pin 2
#define LED_PIN 8
#define NUM_LEDS 60
CRGB leds[NUM_LEDS];

float sampling_period  = 200;
float duty_cycle  = 1;
int duration  = 5;
float t_on = duty_cycle * sampling_period;
float t_off = sampling_period - t_on;
float total_v; // variable to store the running total for voltage for the duty cycle
float total_c;
float cum_energy = 0; // cumulative energy
unsigned long starttime;
float frequency;
float avg_current;
float avg_voltage;
float inst_power;
float energy;
int val;

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

void cycle(int runtime){
  unsigned long stime = millis();

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

    digitalWrite(PWM_Pin, LOW);

    avg_current = duty_cycle * (total_c / (t_on/(duration * 2)));
    if(avg_current < 0){
      avg_current = -avg_current;
    }

    avg_voltage = duty_cycle * (total_v / (t_on/(duration * 2)));

    inst_power = avg_current * avg_voltage;

    energy = inst_power * ((float)sampling_period/1000);

    cum_energy = cum_energy + energy;

    frequency = 0.3173*avg_voltage + 0.6604; // Equation for frequency was taken from testing

    val = map(avg_voltage, 0, 150, 0, NUM_LEDS); // here voltage is being mapped to the LED strip not power
    for(int i = 0; i < val; i++){
      leds[i] = CRGB::Blue;
      FastLED.show();
    }

    Serial.print(avg_current, 2); Serial.print(","); Serial.print(avg_voltage, 2); Serial.print(","); Serial.print(inst_power, 2);
    Serial.print(","); Serial.print(cum_energy, 2); Serial.print(","); Serial.print(frequency, 1); Serial.print(","); /*Serial.print(remaining, 1)*/;
    Serial.println("");
    delay(t_off);
  }
}
void setup() {
  // put your setup code here, to run once:
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  pinMode(PWM_Pin, OUTPUT);
  digitalWrite(PWM_Pin, HIGH);

  Serial.begin(9600);
  //analogReference(EXTERNAL);
  //delay(5000);
  cycle(10000);
  Serial.println("Done");

}

void loop() {
}
