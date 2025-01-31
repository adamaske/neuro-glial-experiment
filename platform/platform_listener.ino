#include <Wire.h>


void setup(){

    // Establish connection with controller

    Serial.writeString("platform:on");

    String response = Serial.readString();
    response.trim();

    // Parse response
    if(response == "")
}