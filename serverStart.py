from data.serverInfo import ServerInfo, InfoReader
from utils.ServerCommons import ServerComms

# "192.168.0.21"
class UDPpositionSever:
    """Base class for UDP Position Server"""

    def __init__(self) -> None:
        self.hostIP = ServerInfo.localHostIP
        self.port = ServerInfo.port

        self.session_status = True

    def start(self) -> None:
        """Start server"""

        sock = ServerComms(
            udpIP=self.hostIP,
            portNUMsnd=self.port,
            portNUMrcv=26951,
            enableTHR=True,
            suppressWarns=True,
            validateConnection=True
        )

        positionVec = "[0, 1, 1]"

        while self.session_status:
            sock.SendPosition(positionVec)
            sock.ValidateConnection()

        
        


s = UDPpositionSever()
s.start()
