import sys
import struct
from typing import List

from serial import SerialException
from pymavlink import mavutil

from Server import Server
from data.serverInfo import ServerInfo
from utils.ServerCommons import ServerComms
# from utils.TelemetryHandler import TelemetryHandler


class UDPpositionSever(Server):
    """Base class for UDP Position Server"""

    def __init__(self) -> None:
        self._hostIP = ServerInfo.localHostIP
        self._remoteIP = ServerInfo.remoteIP
        self._port = ServerInfo.port

        self._session_status = True

        try:
            self.droneConnection = mavutil.mavlink_connection('com7', baud=57600, zero_time_base=True, retires=0) # assuming usage of radio modem
        except SerialException:
            self.droneConnection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600, zero_time_base=True, retires=0) # assuming usage of radio modem

        self.Request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 100)
        # self.droneConnection.mav.request_data_stream_send(self.droneConnection.target_system, 
        #     self.droneConnection.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)

    def start(self) -> None:
        """Start server"""

        sock = ServerComms(
            udpIP=self._hostIP,
            portNUMsnd=self._port,
            portNUMrcv=26951,
            enableTHR=False,
            suppressWarns=True,
            validateConnection=False
        )

        while self._session_status:
            vector_of_angles = self.ReceiveTelemetry()
            self.SendTelemetryUDP(sock=sock, vector=vector_of_angles)

    def ReceiveTelemetry(self) -> bytes:
        """Receives telemetry from the drone"""

        while self._session_status:
            try:
                attitude_data = self.droneConnection.recv_match(type="ATTITUDE" ,blocking=True).to_dict()
                return struct.pack("fff", attitude_data['pitch'], attitude_data['roll'], attitude_data['yaw'])
            except:
                pass

    def Request_message_interval(self, message_id: int, frequency_hz: float):
            
            self.droneConnection.mav.command_long_send(
                self.droneConnection.target_system, self.droneConnection.target_component,
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
                message_id, 
                1e6 / frequency_hz,
                0, 0, 0, 0, 
                0, 
            )

    def SendTelemetryUDP(self, sock: 'utils.ServerCommons.ServerComms', vector: bytes) -> None:
        """
        Sends a vector of positions in Unity coordinate system
        and other crucial data
        """
        sock.SendPosition(vector, self._remoteIP, self._port)
        # sock.ValidateConnection()

    def closeConnection(self, sock: 'utils.ServerCommons.ServerComms') -> None:
        """Closes connection with client"""
        print("Connection closing...")
        sock.CloseConnection(self)


if __name__ == "__main__":
    s = UDPpositionSever()
    s.start()
