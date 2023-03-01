import struct
import argparse
from typing import List
from math import cos

from serial import SerialException
from pymavlink import mavutil

from Server import Server
from data.serverInfo import ServerInfo
from utils.ServerCommons import ServerComms


class UDPpositionSever(Server):
    """Base class for UDP Position Server"""

    def __init__(self, latitude: float, longtitude: float, altitude: float) -> None:

        self._homeLat = latitude
        self._homeLong = longtitude
        self._homeAlt = altitude

        self._hostIP = ServerInfo.localHostIP
        self._remoteIP = ServerInfo.remoteIP
        self._port = ServerInfo.port

        self._session_status = True

        try:
            self.droneConnection = mavutil.mavlink_connection('com7', baud=57600, zero_time_base=True, retires=0) # com port of radio modem on Windows
        except SerialException:
            self.droneConnection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600, zero_time_base=True, retires=0) # com port of radio modem on Linux

        self.Request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE, 100)
        # self.droneConnection.mav.request_data_stream_send(self.droneConnection.target_system, 
        #     self.droneConnection.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 10, 1)
        print(self._homeLat, self._homeLong, self._homeAlt)

    def calculateDistance(self ,lat: float, lng: float, alt: float) -> List[float]:
        """
        Calculates the distance between two points on the Earth
        """

        r = 6371 # earth's radius [km]
        
        x = r * lng * cos(self._homeLong)
        y = r * lat
        z = self._homeAlt - alt
        return [x, y, z]

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
            print(vector_of_angles)
            self.SendTelemetryUDP(sock=sock, vector=vector_of_angles)

    def ReceiveTelemetry(self) -> bytes:
        """
        Receives telemetry from the drone
        angular data is in [rad]
        altitude from GPS is in [mm] both normal and relative
        """
        
        while self._session_status:
            try:
                angular_data = self.droneConnection.recv_match(type="ATTITUDE" ,blocking=True).to_dict()
                position_data = self.droneConnection.recv_match(type='GLOBAL_POSITION_INT', blocking=True).to_dict()
                position_data = self.calculateDistance(position_data['latitude'], position_data['longtitude'], position_data['relative_altitude'])
                print(position_data)
                return struct.pack("fff", angular_data['pitch'], angular_data['roll'], angular_data['yaw'])
                # return struct.pack("ffffff", angular_data['pitch'], angular_data['roll'], angular_data['yaw'], position_data[0], position_data[1], position_data[2])
            except:
                pass
        '''
        while self._session_status:
            try:
                vector_list = [0, 0, 0, random.random(), random.random(), random.random()]
                print(vector_list)
                return struct.pack("ffffff", vector_list[0], vector_list[1], vector_list[2], vector_list[3], vector_list[4], vector_list[5])
            except:
                pass
        '''

    def Request_message_interval(self, message_id: int, frequency_hz: float) -> None:
            
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


def main(args: argparse.Namespace) -> None:

    latitude = args.latitude
    longtitude = args.longtitude

    try:
        altitude = args.altitude
    except AttributeError:
        altitude = 100 # meters above the sea level

    server = UDPpositionSever(latitude, longtitude, altitude)
    server.start()

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Launch positioning server for HoloLens2 Unity client", argument_default=argparse.SUPPRESS, allow_abbrev=False, add_help=False)
    parser.add_argument("--latitude", type=float, help="set latitude")
    parser.add_argument("--longtitude", type=float, help="set longtitude")
    parser.add_argument("--altitude", type=float, help="set altitude. If blank then Warsaw's altitude chosen")
    parser.add_argument("-h", "--help", action="help", help="Display this message")

    args = parser.parse_args()
    main(args)
