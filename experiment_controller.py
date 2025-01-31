#TASKS


#task 1 : COLLECT PRESSURE RATING FROM ARDUINO
import serial
import time

# Set up serial connection
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace COM3 with your port

time.sleep(2)  # Wait for the connection to establish

def send_data(data):
    arduino.write(f"{data}\n".encode())  # Send data to Arduino
    time.sleep(0.1)  # Short delay for Arduino to process
    response = arduino.readline().decode().strip()  # Read response
    return response

# Example usage
print(send_data("Hello Arduino"))


#task 2 : TELL THE ROBOT TO START WHAT TASK


#