import socket
from socket import *

from data.serverInfo import ServerInfo, InfoReader


class UDPpositionSever:
    """Base class for UDP Position Server"""

    def __init__(self) -> None:
        self.hostIP = ServerInfo.localHostIP
        self.port = ServerInfo.port
        self.buffSize = ServerInfo.dataBufferSize

    def start(self) -> None:
        """Start"""

        print("Server starting...")
        
        # UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.bind((self.hostIP, self.port))

        tcp_socket.listen(1)

        # UDPServerSocket.bind((self.hostIP, self.port))

        print("Waiting for connections...")

        while True:
            connection, client = tcp_socket.accept()
            try:
                print(f"Connected to client IP: {client}")
            finally:
                connection.close()

        '''
        while(True):

            bytesAddressPair = UDPServerSocket.recvfrom(self.buffSize)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientIP  = "Client IP Address:{}".format(address)
    
            print(clientIP)
        '''


s = UDPpositionSever()
s.start()
