// This is code the will sense ac current and voltage around a PWM period of 200ms
#define Current_In_Pin A0
#define Voltage_In_Pin A1
#define PWM_Pin 2
int sampling_period  = 200;
int duty_cycle  = 0.5;
int duration  = 5;
int t_on = duty_cycle * sampling_period;
int t_off = sampling_period - t_on;

void SampleCurrent(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float transducer_ref = 2.5;
  float reference_voltage = 5;
  float primary_current = 0;
  float nominal_current = 15;
  float total = 0;
  float sample_time = 0.1;

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Current_In_Pin);
    adc_voltage = adc_value * reference_voltage / 1024;
    primary_current = (nominal_current * (adc_voltage - transducer_ref)) / 0.625;
    total += primary_current; 
    delay(sample_time);
  }

  float avg_current = total / (duration/sample_time);
  Serial1.println(avg_current, 5);
}

int SampleVoltage(int duration) {
  int adc_value = 0;
  float adc_voltage = 0;
  float reference_voltage = 5;
  float voltage_max = 150.5;
  float total = 0;
  float sampling_p = 0.1;

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= duration){
    adc_value = analogRead(Voltage_In_Pin); // between 0 and 1023
    float voltage_in = adc_value * voltage_max / 1024.0; // voltage value between 0 and 150.5 V
    total = total + voltage_in;
    delay(sampling_p);
    endtime = millis();
  }

  float avg_voltage = (total / (duration / sampling_p));
  return avg_voltage;
}


void setup() {
  // put your setup code here, to run once:
  pinMode(PWM_Pin, OUTPUT);
  digitalWrite(PWM_Pin, HIGH);
  Serial1.print("Start");
  Serial1.begin(9600);
  Serial2.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  int total_v = 0; // variable to store the running total for voltage for the duty cycle
  digitalWrite(PWM_Pin, HIGH);

  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= t_on){ // sample current and voltage whilst duty cycle is high
    SampleCurrent(duration);
    total_v += SampleVoltage(duration);
  }
  digitalWrite(PWM_Pin, LOW);

  while((endtime - starttime) <= sampling_period){
    SampleCurrent(duration);
  }

  int avg_voltage = total_v / (t_on/duration);
  Serial2.println(avg_voltage, 5); // send voltage to python averaged over the 200 ms period

}
