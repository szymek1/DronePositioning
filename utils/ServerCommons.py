from builtins import WindowsError
import socket
import threading

from data.serverInfo import ServerInfo


class ServerComms:
    """
    Commons tools for establishing connection with
    Unity client
    """

    def __init__(self, udpIP, portNUMsnd, portNUMrcv, enbaleTHR=False, suppressWarns=False) -> None:
        """
        -udpIP: any IP to connect to
        -portNUMsnd: a port related to the IP above to send
        -portNUMrcv: a port to receive info
        -enableTHR: if False then only sending from Python, not receiving
        -suppressWarns: if False not sending warnings about connection
        """

        self.udpIP = udpIP
        self.udpSendPort = portNUMsnd
        self.udpRcvPort = portNUMrcv
        self.enableTHR = enbaleTHR
        self.suppressWarns = suppressWarns

        self.isDataRcvd = False
        self.dataRCVD = None

        # establishing UDP connection
        self.udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpSock.bind((udpIP, portNUMrcv))

        # if enableTHR=True then create receiving thread
        if enbaleTHR:
            self.rcvTHr = threading.Thread(target=self.RcvThreadFunc, daemon=True)
            self.rcvTHr.start()

    def __del__(self) -> None:
        """Deletes socket"""

        self.CloseConnection()

    def CloseConnection(self) -> None: 
        """Functionality to delete socket"""

        self.udpSock.close()

    def  SendPosition(self, data: str) -> None:
        """Sends encoded position vector"""

        self.udpSock.sendto(bytes(data, "utf-8"), 
                           (self.udpIP, self.udpSendPort))

    def ReceiveData(self) -> str:
        """Returns data if it came from the system"""

        if not self.enableTHR:
            raise ValueError("Receiving data not enabled!")

        data_from_system = None
        self.systemIP = None

        try:
            data_from_system, self.systemIP = self.udpSock.recvfrom(ServerInfo.dataBufferSize)
            data_from_system = data_from_system.decode("utf-8")
        except WindowsError as err:
            if err.winerror == 10054:
                if not self.suppressWarns:
                    print("Connect to the system!")
                else:
                    pass
            else:
                raise ValueError("Cannot convert data to string")

        return data_from_system

    def RcvThreadFunc(self) -> None:
        """Checks if data received from the system is available"""

        self.isDataRcvd = False

        while True:
            dataRcvd = self.ReceiveData()
            self.dataRCVD = dataRcvd
            self.isDataRcvd = True

    def ValidateConnection(self) -> bool:
        """Validates connection to the system"""

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
            print(f"[CONNECTION INFO] connected to: {connectedIP}")
            return True

        return False
        