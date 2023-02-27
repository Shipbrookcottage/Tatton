#define Analog_In_Pin A1

int adc_value = 0;
float adc_voltage = 0;
float reference_voltage = 5;
float voltage_max = 150.5;
float total = 0;


void setup() {
  // put your setup code here, to run once:
  // Setup Serial Monitor
   Serial.begin(9600);
   Serial.println("DC Voltage Test");

}

void loop() {
  // Read the Analog Input
  float starttime = millis();
  float endtime = starttime;

  while((endtime - starttime) <= 5000){
    adc_value = analogRead(Analog_In_Pin); // between 0 and 1023
    float voltage_in = adc_value * voltage_max / 1024.0; // voltage value between 0 and 1 V
    total = total + voltage_in;
    delay(1);
    endtime = millis();
  }

  float avg_voltage = total / 5000;
  total = 0;

  Serial.print("Average Voltage = ");
  Serial.println(avg_voltage, 5);







}