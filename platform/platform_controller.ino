
#include <Wire.h>          // What does this do ?
#include <AccelStepper.h>  // Library created by Mike McCauley at http://www.airspayce.com/mikem/arduino/AccelStepper/
#define STEP_PIN 2
#define DIR_PIN 5

// Gyroscope
float g_time = 0;  // Time
float g_elapsed_time = 0;
float g_previous_time = 0;
float g_raw_x = 0;  // Data
float g_raw_y = 0;
float g_raw_z = 0;
int g_error = 0;  // Errors
float g_raw_error_x = 0;
float g_raw_error_y = 0;
float g_raw_error_z = 0;
float g_angle_x = 0;  // Angles
float g_angle_y = 0;
float g_angle_z = 0;
void calibrate_gyroscope(int rounds);
void handle_gyroscope();
void print_gyroscope();

// Accelerometer
int a_error = 0;
float a_raw_x = 0;
float a_raw_y = 0;
float a_raw_z = 0;
float a_angle_x = 0;
float a_angle_y = 0;
float a_angle_z = 0;
float a_angle_error_x = 0;
float a_angle_error_y = 0;
float a_angle_error_z = 0;
float a_total_angle_x = 0;
float a_total_angle_y = 0;
float a_total_angle_z = 0;
void calibrate_accelerometer(int rounds = 200);
void handle_accelerometer();
void print_accelerometer();


// Potentiometer
int p_value = 0;     // Analog reading
int p_filtered = 0;  // Filtered analog reading
int p_previous = 0;
int p_new = 0;  // Dont know
float p_smoothing = 1;
void handle_potentionmeter();
void print_potentionmeter();

// Steppermotor
AccelStepper stepper(1, STEP_PIN, DIR_PIN);
int s_acceleration = 2000;
int s_max_speed = 2000;
void config_stepper();
void handle_stepper();
void print_stepper();

float rad_to_deg = 180 / 3.141592654;
void print();

void setup() {
  Wire.begin();

  Wire.beginTransmission(0x68);  // begin, Send the slave adress (in this case 68)
  Wire.write(0x6B);              // make the reset (place a 0 into the 6B register)
  Wire.write(0x00);
  Wire.endTransmission(true);  // end the transmission

  //Gyro config
  Wire.beginTransmission(0x68);  // begin, Send the slave adress (in this case 68)
  Wire.write(0x1B);              // We want to write to the GYRO_CONFIG register (1B hex)
  Wire.write(0x10);              // Set the register bits as 00010000 (1000dps full scale)
  Wire.endTransmission(true);    // End the transmission with the gyro

  //Acc config
  Wire.beginTransmission(0x68);  // Start communication with the address found during search.
  Wire.write(0x1C);              // We want to write to the ACCEL_CONFIG register
  Wire.write(0x10);              // Set the register bits as 00010000 (+/- 8g full scale range)
  Wire.endTransmission(true);

  // Stepper config
  config_stepper();
  stepper.setMaxSpeed(s_max_speed);      // Set speed fast enough to follow pot rotation --- acces
  stepper.setAcceleration(s_acceleration);  // High Acceleration to follow pot rotation  --- acces

  Serial.begin(9600);  // Remember to set this same baud rate to the serial monitor
  g_time = millis();   // Start counting time in milliseconds

  calibrate_gyroscope(200);
  calibrate_accelerometer(200);
}

void loop() {
  handle_potentionmeter();  // tells motor to rotate if potentiomter crossed
                            // across threshold
  handle_gyroscope(); 
  handle_gyroscope(); // 
  handle_stepper();
}

void calibrate_gyroscope(int rounds) {
  g_previous_time = g_time;
  g_time = millis();
  g_elapsed_time = (g_time - g_previous_time) / 1000.0;  // 1000 -> millisec to seconds

  for (int i = 0; i < rounds; i++) {
    Wire.beginTransmission(0x68);
    Wire.write(0x43);  // gyro register ->
    Wire.endTransmission(false);
    Wire.requestFrom(0x68, 4, true);  //ask for 4 registers

    g_raw_x = Wire.read() << 8 | Wire.read();
    g_raw_y = Wire.read() << 8 | Wire.read();

    g_raw_error_x = g_raw_error_x + (g_raw_x / 32.8);
    g_raw_error_y = g_raw_error_y + (g_raw_y / 32.8);
  }

  g_raw_error_x = g_raw_error_x / (float)rounds;
  g_raw_error_y = g_raw_error_y / (float)rounds;
  g_error = 1;
};

void handle_gyroscope() {
  Wire.beginTransmission(0x68);
  Wire.write(0x43);  // gyro register ->
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 4, true);  //ask for 4 registers

  g_raw_x = Wire.read() << 8 | Wire.read();
  g_raw_y = Wire.read() << 8 | Wire.read();

  g_raw_x = (g_raw_x / 32.8) - g_raw_error_x;
  g_raw_y = (g_raw_y / 32.8) - g_raw_error_y;

  g_angle_x = g_raw_x * g_elapsed_time;
  g_angle_y = g_raw_y * g_elapsed_time;
}

void print_gyroscope() {
}

void calibrate_accelerometer(int rounds) {
  for (int i = 0; i < rounds; i++) {
    Wire.beginTransmission(0x68);
    Wire.write(0x3B);  // 0x3B -> acc_x register
    Wire.endTransmission(false);
    Wire.requestFrom(0x68, 6, true);  // 6 registers

    a_raw_x = (Wire.read() << 8 | Wire.read()) / (float)4096;
    a_raw_y = (Wire.read() << 8 | Wire.read()) / (float)4096;
    a_raw_z = (Wire.read() << 8 | Wire.read()) / (float)4096;

    a_angle_error_x = a_angle_error_x + atan(a_raw_y / sqrt(pow(a_raw_x, 2) + pow(a_raw_z, 2))) * rad_to_deg;
    a_angle_error_y = a_angle_error_y + atan(-a_raw_x / sqrt(pow(a_raw_y, 2) + pow(a_raw_z, 2))) * rad_to_deg;
  }

  a_angle_error_x = a_angle_error_x / (float)rounds;
  a_angle_error_y = a_angle_error_y / (float)rounds;
  a_error = 1;
}

void handle_accelerometer() {
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);  // 0x3B -> acc_x register
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true);  // 6 registers

  a_raw_x = (Wire.read() << 8 | Wire.read()) / (float)4096;
  a_raw_y = (Wire.read() << 8 | Wire.read()) / (float)4096;
  a_raw_z = (Wire.read() << 8 | Wire.read()) / (float)4096;

  a_angle_x = (atan(a_raw_y / sqrt(pow(a_raw_x, 2) + pow(a_raw_z, 2))) * rad_to_deg) - a_angle_error_x;
  a_angle_y = (atan(-a_raw_x / sqrt(pow(a_raw_x, 2) + pow(a_raw_z, 2))) * rad_to_deg) - a_angle_error_y;

  a_total_angle_x = 0.98 * (a_total_angle_x + g_angle_x) + 0.02 * a_angle_x;
  a_total_angle_y = 0.98 * (a_total_angle_y + g_angle_y) + 0.02 * a_angle_y;
}

void print_accelerometer() {
  Serial.print("Xº: ");
  Serial.print(a_total_angle_x);
  Serial.print("   |   ");
  Serial.print("Yº: ");
  Serial.print(a_total_angle_y);
}


void config_stepper(){

}
void handle_stepper(){ // Listen for serial input from controller
  String str = Serial.readString();
  str.trim();

  //Parse str
  char size = str[0]; // byte 0 tells about the incoming message
  

}
void print_stepper(){

}

void handle_potentionmeter() {
  p_value = analogRead(A0);  // Reads potentiometer
  p_filtered = (p_value * p_smoothing) + (1 - p_smoothing) * p_filtered;

  bool moved = abs(p_filtered - p_previous) >= 70;
  if (!moved)
    return;

  p_new = map(p_filtered, 0, 1023, 10000, 0);
  stepper.runToNewPosition(p_new);
  p_previous = p_filtered;
}

void print_potentiometer() {
  Serial.print(" Filtered Value: ");
  Serial.print(p_filtered);
  Serial.println(" ");
}


void print() {  // Generic printing
}