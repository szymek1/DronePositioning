import struct
from typing import List
from math import degrees

from pymavlink import mavutil

from Server import Server
from data.serverInfo import ServerInfo
from utils.ServerCommons import ServerComms
# from utils.TelemetryHandler import TelemetryHandler


class UDPpositionSever(Server):
    """Base class for UDP Position Server"""

    def __init__(self) -> None:
        self._hostIP = ServerInfo.localHostIP
        self._port = ServerInfo.port

        self._session_status = True

        self.droneConnection = mavutil.mavlink_connection('com7', baud=57600)

        self.droneConnection.mav.request_data_stream_send(self.droneConnection.target_system, 
            self.droneConnection.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 1000, 1)

    def start(self) -> None:
        """Start server"""

        sock = ServerComms(
            udpIP=self._hostIP,
            portNUMsnd=self._port,
            portNUMrcv=26951,
            enableTHR=True,
            suppressWarns=True,
            validateConnection=True
        )

        while self._session_status:
            # print("Sending...")
            vector_of_angles = self.ReceiveTelemetry()
            # print(vector_of_angles)
            self.SendTelemetryUDP(sock=sock, vector=vector_of_angles)

    def ReceiveTelemetry(self) -> bytes:
        """Receives telemetry from the drone"""
        # TH = TelemetryHandler()
        # return TH.reciveTelemetry(self._session_status)
        while self._session_status:
            attitude_data = self.droneConnection.recv_match(type="ATTITUDE" ,blocking=True).to_dict()
            # angles = [
            #     attitude_data['roll'],
            #     attitude_data['pitch'],
            #     attitude_data['yaw']
            # ]
            # print(attitude_data['roll'], attitude_data['pitch'], attitude_data['yaw'])
            return struct.pack("fff", attitude_data['roll'], attitude_data['pitch'], attitude_data['yaw'])

    def SendTelemetryUDP(self, sock: 'utils.ServerCommons.ServerComms', vector: str) -> None:
        """
        Sends a vector of positions in Unity coordinate system
        and other crucial data
        """
        sock.SendPosition(vector)
        sock.ValidateConnection()

    def closeConnection(self, sock: 'utils.ServerCommons.ServerComms') -> None:
        """Closes connection with client"""
        print("Connection closing...")
        sock.CloseConnection(self)

        
        


s = UDPpositionSever()
s.start()
