void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  

}

//pressure sensor -> Connected to an analog input 0 
int ps_apin = 0; //analog pin
int ps_voltage_divider_ohm = 10000; //ohm
int ps_voltage_millivolts = 5000;
int pressure_reading(){
  int reading = readAnalog(ps_apin);

  //                 input, 0 to 1023 -> 0 to 5000 millivolts
  int voltage = map(reading, 0, 1023, 0, 5000); 
  int voltage_over_sensor = (ps_voltage_millivolts - voltage)
  int resistance = (voltage_over_sensor * ps_voltage_divider_ohm) / ps_voltage_millivolts;

  return 0;
}