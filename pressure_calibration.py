import socket
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch
import datetime
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the lowest level to capture all messages
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to the console
    ]
)
def run_ur_server(run_time=3):
    # UR3 Connection - TCP Server
    ur_server_ip = "10.47.20.11" # use "ipconfig"  to get this ip
    ur_server_port = 32000 #
    # NOTE : This ip, and port must be set in the UR3 program "Before Start" module -> socket_open(ip, port)
    ur_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP server
    ur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # NOTE : Dont use, reserved for connection
    ur_server.bind((ur_server_ip, ur_server_port))
    print(f"TCP server established on {ur_server_ip} : {ur_server_port}")

    print(f"Please establish the UR3 TCP connection before starting experiment : ")
    ur_server.listen(1)
    print(f"TCP server listening on {ur_server_ip}:{ur_server_port} and waiting for UR3 connection...")
    ur_socket, ur_address = ur_server.accept()
    print(f"Connection established with UR3 : {ur_address}.")


    pressure_readings = []
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = run_time - elapsed_time
        
        if remaining_time <= 0:
            break
        
        data = ur_socket.recv(1024)

        msg = data.decode()
        print(f"RECEIEVED FROM ROBOT : {msg}")
        logging.info("MESSAGE : " + msg)
        
        #pressure = int.from_bytes(data, "big")
        #pressure_readings.append(pressure)

        #print(f"Reading : {pressure} | Remaining time : {remaining_time:.2f} seconds...")
    
    #pressure_readings = np.array(pressure_readings)
    #np.save("data/" + datetime.datetime.now().strftime("%d_%M_%Y_%S_%M_%H") + "_pressure", pressure_readings)
    return pressure_readings

def analyze(signal, run_time):

    #  we captured our signal, now we need to inspect it. 
    signal = np.array(signal) # turn to numpy
    fs = len(signal) / run_time # find the sampling frequency

    # Generate a sample signal with noise
    t = np.linspace(0, run_time, int(fs*run_time), endpoint=False)  # Linear space for the signal

    # Add random Gaussian noise
    noise = np.random.normal(0, 0.5, signal.shape)  # Mean 0, Std 0.5
    x = signal + noise 

    # Perform FFT
    fft_result = np.fft.fft(x)
    frequencies = np.fft.fftfreq(len(x), d=1/fs)

    # Compute PSD using Welch’s method
    f_psd, psd = welch(x, fs, nperseg=256)

    plt.figure(figsize=(12, 6))
    plt.subplot(3, 1, 1)
    plt.plot(t, signal)
    plt.title("UR3 Force - Torque - Pressure (Newton) ")
    plt.ylabel("Magnitude (Newtwon)")
    plt.xlabel("Time (Seconds)")

    # Plot FFT
    plt.subplot(3, 1, 2)
    plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_result[:len(frequencies)//2]))
    plt.title("FFT Analysis with Noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()

    # Plot PSD
    plt.subplot(3, 1, 3)
    plt.semilogy(f_psd, psd)
    plt.title("Power Spectral Density (PSD) with Noise")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power")
    plt.grid()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    duration = 30
    run_ur_server(30)
    #for i in range(1):
    #    pressure = run_ur_server(duration)
    #    analyze(pressure, duration)
#
    exit()
    signals = []
    for file in os.listdir("data"):
        signal = np.load(file=os.path.join("data", file))
        signals.append(signal)
    for signal in signals:
        analyze(signal, duration)


        #analysis = analyze(pressure, duration)

