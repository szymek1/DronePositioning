import socket
import threading
from typing import Tuple
# from builtins import WindowsError

from data.serverInfo import ServerInfo


class ServerComms:
    """
    Commons tools for establishing connection with
    Unity client
    """

    def __init__(self, udpIP, portNUMsnd, portNUMrcv, enableTHR=True, suppressWarns=False, validateConnection=True) -> None:
        """
        -udpIP: any IP to connect to
        -portNUMsnd: a port related to the IP above to send
        -portNUMrcv: a port to receive info
        -validateConnection: if True then server logs information about connection established with the system
        -suppressWarns: if False not sending warnings about connection
        """

        self.udpIP = udpIP
        self.udpSendPort = portNUMsnd
        self.udpRcvPort = portNUMrcv
        self.enableTHR = enableTHR
        self.suppressWarns = suppressWarns
        self.validateConnection = validateConnection

        self.isDataRcvd = False
        self.dataRCVD = None
        self.systemIP = None

        # establishing UDP connection
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpSock.bind((udpIP, portNUMrcv))

        # if validateConnection=True then create receiving thread
        if enableTHR:
            self.rcvTHr = threading.Thread(target=self.RcvThreadFunc, daemon=True)
            self.rcvTHr.start()

    def __del__(self) -> None:
        """Deletes socket"""
        self.CloseConnection()

    def CloseConnection(self) -> None: 
        """Functionality to delete socket"""
        self.udpSock.close()

    def  SendPosition(self, data: bytes, remoteIP: str, remotePort: int) -> None:
        """Sends encoded position vector"""

        self.udpSock.sendto(data, (remoteIP, remotePort))

    def ReceiveData(self) -> Tuple[str, tuple]:
        """Returns data if it came from the system"""

        if not self.enableTHR:
            raise ValueError("Receiving data not enabled!")

        data_from_system = None
        systemIP = None

        try:
            data_from_system, systemIP = self.udpSock.recvfrom(ServerInfo.dataBufferSize)
            data_from_system = data_from_system.decode("utf-8")
        except Exception as err:
            if not self.suppressWarns:
                print("Connect to the system!")
            '''
            if err.winerror == 10054:
                if not self.suppressWarns:
                    print("Connect to the system!")
                else:
                    pass
            else:
                raise ValueError("Cannot convert data to string")
            '''

        return data_from_system, systemIP

    def RcvThreadFunc(self) -> None:
        """Checks if data received from the system is available"""

        self.isDataRcvd = False

        while True:
            dataRcvd, con_info = self.ReceiveData()
            self.dataRCVD = dataRcvd
            self.systemIP = con_info
            self.isDataRcvd = True

    def ValidateConnection(self) -> None:
        """Validates connection to the system"""

        if self.validateConnection:

            data = None
            connectedIP = None
            validation_val = "1"

            if self.isDataRcvd:
                self.isDataRcvd = False
                data = self.dataRCVD
                self.dataRCVD = None

                connectedIP = self.systemIP
                self.systemIP = None
            
            if data == validation_val:
                print(f"[CONNECTION INFO] connected to: {connectedIP[0]}:{connectedIP[1]}")
            '''
            TODO:
            - make server to shutdown after given time without the connection
            '''
        
        else:
            raise ValueError("Connection validation not enabled!")