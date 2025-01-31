
import serial
import time
import logging


bdrate = 9600
serial_port = 'COM4'

arduino = serial.Serial(port=serial_port, baudrate=bdrate, timeout=3)


def write_read(x) -> (bytes|None):
    
    arduino.write(bytes(x, 'utf-8'))
    
    time.sleep(0.05)
    
    data = arduino.readline()
    
    return data

def write_serial(x) -> (int|None):
    result = arduino.write(bytes(x, 'utf-8'))
    if result is None:
        logging.warning('Writing to serial failed...')
    else:
        logging.info('wrote to serial: ', result, ' bytes')
    return result

if __name__ == "__main__":

    #establish connection

    # 1. Tell the motor how to turn -> adjust the position of the wedge
    # and adjusts the angle of the stepping platform
    
    # 2. Inspect and validate the data from the gyroscope and accelerometer
    
    # 3. Launch the pnematic system
    
    
    write_serial("SM:34")
    
    
