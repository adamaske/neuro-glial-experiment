import socket
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

# UR3 Connection - TCP Server
ur_server_ip = "192.168.50.53" # use "ipconfig"  to get this server
ur_server_port = 32000 #
# NOTE : This ip, and port must be set in the UR3 program "Before Start" module -> socket_open(ip, port)
ur_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP server
ur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # NOTE : Dont use, reserved for connection
print(f"TCP server established on {ur_server_ip} : {ur_server_port}")

if False:
    print(f"Please establish the UR3 TCP connection before starting experiment : ")
    ur_server.listen(1)
    print(f"TCP server listening on {ur_server_ip}:{ur_server_port} and waiting for UR3 connection...")
    ur_socket, ur_address = ur_server.accept()
    print(f"Connection established with UR3 : {ur_address}.")


pressure_readings = []

run_time = 2.0

start_time = time.time()
while time.time() - start_time < run_time:
    
    if False:
        data = ur_socket.recv(1024)
        pressure = int.from_bytes(data)
    else:
        time.sleep(0.01) # Fake 20 Hz frequency
        pressure = float(np.random.random()) * 100 # Random number between 0 and 100
        pressure_readings.append(pressure)

#  we captured our signal, now we need to inspect it. 
signal = np.array(pressure_readings) # turn to numpy
fs = len(signal) / run_time # find the sampling frequency

# Generate a sample signal with noise
t = np.linspace(0, run_time, int(fs*run_time), endpoint=False)  # Linear space for the signal
signal =  np.sin(2 * np.pi * 3 * t) + (0.5 * np.sin(2 * np.pi * 7 * t))

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
plt.title("Original Signal")
plt.ylabel("Magnitude")
plt.xlabel("Time")

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