
import os
import time
import datetime
import socket
import logging
import threading
import json
from pylsl import StreamInfo, StreamOutlet

#What remains ? 

# Experiment
experiment_name = "ADEPT Heel".replace(" ", "_")
conducted_time = datetime.datetime.now()
subject_id = 0
trial_number = 1

# Block Design
blocks = [ "Rest", "Stimuli" ]
durations = [ 3, 5 ] # Seconds
block_order = [ 0, 1, 0, 1] # NOTE : This are indices into the Blocks array
wait_for_input_blocks = [ False, False ] # If True : to proceed to next block, a manual input is needed


use_fnirs = True # 
use_eeg = True # 
use_ur3 = False # NOTE : This requires the program to wait for an accepted connection before experiment can start


def validate_block_design(): # NOTE : This verifies your block design is possible to complete
    assert(len(durations) == len(blocks)) # Each block needs a duration
    for block_idx in block_order: 
        assert(block_idx >= 0) # The block index must be inside the bounds of the Blocks array,
        assert(block_idx < len(blocks)) # 0 < idx < len(Blocks)
    assert(len(wait_for_input_blocks) == len(blocks)) # Each block must either manually or automatically proceed
validate_block_design()

def print_experiment_description():
    print(f"Welcome To Experiment : {experiment_name}")
    print(f"Conducted : {conducted_time.ctime()}")
    print(f"Subject ID : {subject_id}")
    print(f"Trial : {trial_number}")
    order_string = ""
    for elm in block_order:
        order_string = order_string + (blocks[elm] + "->")
    order_string = order_string + "End"
    print("Block Order : ", order_string)
print_experiment_description()  

def save_experiment_to_file():
    encoded = {
        "experiment_name": experiment_name, # Experiment
        "date_time": conducted_time.strftime("%d_%m_%Y_%H_%M_%S"),
        "subject_ID": subject_id,
        "trial_number" : trial_number, 
        
        "blocks" : blocks, # Block Design
        "durations" : durations,
        "block_order" : block_order,
        "block_wait_for_input" : wait_for_input_blocks,
        
        "using_fnirs" : use_fnirs,
        "using_eeg" : use_eeg,
        "use_ur3" : use_ur3,
    }
    filename = experiment_name + "_" + conducted_time.strftime("%d_%m_%Y_%H_%M_%S") + "subject_" + str(subject_id) +  "_trial_" + str(trial_number) + ".json"
    filepath = "logs/" + filename 

    with open(filepath, "w") as json_file:
        json.dump(encoded, json_file, indent=4)
    json_file.close()
save_experiment_to_file()


# Logging
# NOTE : Use logging.debug|info|error|warning to write to screen and console, use printf for only console
log_filename = experiment_name + "_" + conducted_time.strftime("%d_%m_%Y_%H_%M_%S") + "subject_" + str(subject_id) + "_trial_" + str(trial_number) + ".log"
log_filepath = "logs/" + log_filename
logging.basicConfig(
    level=logging.DEBUG,  # Set the lowest level to capture all messages
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath),  # Log to a text file
        logging.StreamHandler()  # Log to the console
    ]
)

# EEG 
# g.Recorder listens to a socket via the Universal Datagram Protocol (UDP)
eeg_target_ip = '127.0.0.1'  # Change this to g.Recorder computer IP address
eeg_target_port = 1000  # Change this to the port set in g.Recorder
eeg_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4 UDP Socket 
logging.info(f"UDP socket established {eeg_target_ip} : {eeg_target_port}")

def fill_grecorder_xml_msg(input): #inser input into XML as required by g.Recorder
    msg = '<gRecorder><DAQ.KeyboardMarkerUdpMessage assembly="gRecorder" name="' + str(input) + '"/></gRecorder>'
    return msg.encode()

# fNIRS
# Aurora is listening to a Lab Streaming Layer (LSL) named "Trigger" of type "Markers"
stream_name = "Triggers"
stream_type = "Markers"
stream_channels = 1
stream_format = "int32"
stream_id = "ADEPT"
fnirs_info = StreamInfo(name=stream_name, 
                        type=stream_type, 
                        channel_count=stream_channels, 
                        channel_format=stream_format, 
                        source_id=stream_id) 
fnirs_outlet = StreamOutlet(fnirs_info) # LSL outlet
logging.info(f"LSL outlet established {stream_name}:{stream_type}, {stream_channels}x{stream_format} @ {stream_id}")

# UR3 Connection - TCP Server
ur_server_ip = "192.168.50.53" # use "ipconfig"  to get this server
ur_server_port = 32000 #
# NOTE : This ip, and port must be set in the UR3 program "Before Start" module -> socket_open(ip, port)
ur_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP server
ur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # NOTE : Dont use, reserved for connection
logging.info(f"TCP server established on {ur_server_ip} : {ur_server_port}")

if use_ur3: 
    print(f"Please establish the UR3 TCP connection before starting experiment : ")
    ur_server.listen(5)
    print(f"TCP server listening on {ur_server_ip}:{ur_server_port} and waiting for UR3 connection...")
    ur_socket, ur_address = ur_server.accept()
    logging.info(f"Connection established with UR3 : {ur_address}.")


def push_block_onset_marker(block_idx:int): # Marks data with the onset of each block.
    if use_fnirs:
        fnirs_outlet.push_sample([block_idx])
    if use_eeg:
        eeg_socket.sendto(fill_grecorder_xml_msg(block_idx), (eeg_target_ip, eeg_target_port)) # NOTE : This is already encoded to bytes
    if use_ur3:
       pass
    logging.debug("Pushed marker : " + str(block_idx))


start = input(f"Press [ ENTER ] to start trial {trial_number}...")


for idx in range(len(block_order)):
    block_start_time = time.time()
    block_idx = block_order[idx]
    current_block = blocks[block_idx]
    block_duration = durations[block_idx]
    
    print("\n\n")
    logging.debug(f"STARTED : {current_block}")
    push_block_onset_marker(block_idx)
    
    
    if wait_for_input_blocks[block_idx]: #Handle manual procedure blocks
        if idx == len(block_order)-1: # Is this the final block?
            proceed = input("Press [ ENTER ] to complete experiment trial...")
            continue
        else:
            proceed = input(f"Press [ ENTER ] to proceed to next block : {blocks[block_order[idx + 1]]}")
            continue
            
    
    while True:
        elapsed_time = time.time() - block_start_time
        remaining_time = block_duration - elapsed_time
        
        if remaining_time <= 0:
            break
        
        if remaining_time <= 3: 
            print(f"Block [ {current_block} ] starting in {remaining_time:.2f} seconds...", end="\r1")
        else: 
            print(f"Remaining time for block {block_idx}: {remaining_time:.2f} seconds..-", end='\r')
        
        
        time.sleep(0.01)  # Sleep to prevent excessive CPU usage
    
    logging.debug(f"ENDED : {current_block}")


logging.debug("Experiment Complete.")