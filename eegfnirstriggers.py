"""Example program to demonstrate how to send string-valued markers into LSL."""

import random

from pylsl import StreamInfo, StreamOutlet
import socket
import time

use_fnirs = True
use_eeg = True
use_robot = True


# EEG -> g.Recorder via UDP 
eeg_target_ip = '127.0.0.1'  # Change this to the desired target IP
eeg_target_port = 1000  # Change this to the desired port number

# Create a UDP socket
eeg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

eeg_messages = [ 
    b'<gRecorder><DAQ.KeyboardMarkerUdpMessage assembly="gRecorder" name="0"/></gRecorder>',
    b'<gRecorder><DAQ.KeyboardMarkerUdpMessage assembly="gRecorder" name="1"/></gRecorder>',
]

#fNIRS -> Aurora via LSL
fnirs_info = StreamInfo(name='Trigger', type='Markers', channel_count=1, channel_format='int32', source_id='Example') 
fnirs_outlet = StreamOutlet(fnirs_info)

#              0,           1,          2,       3      4      
markers = [ "REST", "RIGHT", "LEFT", "END" ]
durations = [ 20, 10, 10]

order = [0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0]

def push_marker(marker_index):
    if use_fnirs:
        fnirs_outlet.push_sample([marker_index])
    if use_eeg:
       eeg_sock.send(eeg_messages[marker_index])

start = input("Press any key to start experiment....")
start_time = time.time()

idx = 0
current_block_idx = 0

running = True
while idx < len(order):
    block_started = time.time()  # When did the current block start
    current_block_idx = order[idx] #find the index in markers list

    print(f"Processing block {markers[current_block_idx]}")
    print(f"SUBJECT EXECUTE : {markers[current_block_idx]}")
    
    push_marker(order[idx])
    while time.time() - block_started < durations[current_block_idx]:
        elapsed_time = time.time() - block_started
        remaining_time = durations[current_block_idx] - elapsed_time
        
        # Print the remaining time (rounded to 2 decimal places)
        print(f"Remaining time for block {current_block_idx}: {remaining_time:.2f} seconds", end='\r')
        time.sleep(0.1)  # Sleep a bit to prevent excessive printing (optional)
        
    idx += 1  # Move to the next block
    print(f"Block {current_block_idx} completed, moving to next.")

push_marker(3) #finished push \end\
print(f"EXPERIMENT COMPLETE")
exit()
