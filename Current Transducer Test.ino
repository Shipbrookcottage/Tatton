
#define Analog_In_Pin A0
int adc_value = 0;
float adc_voltage = 0;
float transducer_ref = 2.5;
float reference_voltage = 5;
float primary_current = 0;
float nominal_current = 15;


void setup() {
  // put your setup code here, to run once:
  // Setup Serial Monitor
   Serial.begin(9600);
   Serial.println("DC Voltage Test");

   // Initiliase parameters
}

void loop() {
  // Read the Analog Input
   adc_value = analogRead(Analog_In_Pin); // between 0 and 1023
   adc_voltage = adc_value * reference_voltage / 1024.0; // voltage value between 0 and 5 V
   primary_current = (nominal_current * (adc_voltage - transducer_ref)) / 0.625;

   Serial.print("Input Current = ");
   Serial.println(primary_current, 5);
   Serial.print("Measured Voltage = ");
   Serial.println(adc_voltage, 5);

   delay(1000);


}
