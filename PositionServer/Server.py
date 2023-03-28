from abc import ABC
from abc import abstractmethod


class Server(ABC):
    """
    Server class with functionalities for both
    sending and receiving drone's telemetry
    """

    @abstractmethod
    def start(self) -> None:
        """Start server"""
        pass

    @abstractmethod
    def ReceiveTelemetry(self) -> None:
        """Receives telemetry from the drone"""
        pass

    @abstractmethod
    def SendTelemetryUDP(self, sock: 'utils.ServerCommons.ServerComms') -> None:
        """
        Sends a vector of positions in Unity coordinate system
        and other crucial data
        """
        pass

    @abstractmethod
    def closeConnection(self, sock: 'utils.ServerCommons.ServerComms') -> None:
        """Closes connection with client"""
        pass
