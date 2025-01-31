
import random
from pylsl import StreamInfo, StreamOutlet
import socket
import time

#wait for start
def fill_grecorder_xml_msg(input):
    msg = '<gRecorder><DAQ.KeyboardMarkerUdpMessage assembly="gRecorder" name="' + str(input) + '"/></gRecorder>'
    return msg

# EEG 
# g.Recorder listens to a socket via the Universal Datagram Protocol (UDP)
eeg_target_ip = '127.0.0.1'  # Change this to g.Recorder computer IP address
eeg_target_port = 1000  # Change this to the port set in g.Recorder
eeg_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4 UDP Socket 

# fNIRS
# Aurora is listening to a Lab Streaming Layer (LSL) named "Trigger" of type "Markers"
fnirs_info = StreamInfo(name='Trigger', 
                        type='Markers', 
                        channel_count=1, # We only have a single channel
                        channel_format='int32', # We're only sending integers
                        source_id='ADEPT') 
fnirs_outlet = StreamOutlet(fnirs_info) # LSL outlet

markers = [ "REST", "PRESSURE THREESHOLD REACHED"]
durations = [ 5, 4, ]
order = [ 0, 1, 0, 1]

assert(len(markers) == len(durations)) #Every marker need a duration

def push_marker(marker_index:int):
    fnirs_outlet.push_sample([marker_index])
    eeg_socket.send(fill_grecorder_xml_msg(marker_index).encode()) # TODO : find correct encoding
    
    print("Pushed marker : [ " + markers[marker_index] + " ]")
    

start = input("Press [ ENTER ] to start experiment...")

import time

for idx in range(len(order)):
    block_start_time = time.time()
    current_block = order[idx]
    block_duration = durations[current_block]
    
    print(f"STARTED BLOCK: [ {markers[current_block]} ]")
    
    while True:
        elapsed_time = time.time() - block_start_time
        remaining_time = block_duration - elapsed_time
        
        if remaining_time <= 0:
            break
        
        
        if remaining_time <= 3: 
            print(f"Block [ {markers[current_block]} ] starting in {remaining_time:.2f} seconds...", end="\r")
        else: 
            print(f"Remaining time for block {current_block}: {remaining_time:.2f} seconds..-", end='\r')
        
        
        time.sleep(0.1)  # Sleep to prevent excessive CPU usage
    
    print(f"\nBLOCK {current_block} completed.")  # Newline to avoid overwriting output

        