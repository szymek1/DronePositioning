import os
import sys

from pymavlink import mavutil


the_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600, zero_time_base=True, retires=0)
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component, 
        mavutil.mavlink.MAV_DATA_STREAM_ALL, 200, 1)


while True:
    msg_position = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True).to_dict()
    msg_angles = the_connection.recv_match(type="ATTITUDE" ,blocking=True).to_dict()

    # msg = the_connection.recv_match(type='LOCAL_POSITION_NED')
    # msg = the_connection.recv_match(type='HOME_POSITION')
    # msg = the_connection.recv_match(type='ATTITUDE')
    # msg = the_connection.messages
    print(msg_position)
    print(msg_angles)
    '''
    msg = the_connection.recv_match(type="ATTITUDE" ,blocking=True).to_dict()
    angles = [
        msg['roll'],
        msg['pitch'],
        msg['yaw']
    ]
    if msg != None:
        print(angles)
    '''