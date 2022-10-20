import socket
import threading
from typing import Tuple


def sendMess(s: socket.socket, rcvrData: Tuple[str, int], sess: bool) -> None:
	mess = bytes("1", "utf-8")
	while sess:
		s.sendto(mess, rcvrData)

localIP = "172.24.160.16"
localPort = 26950

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((localIP, localPort))

session = True

sendTHRD = threading.Thread(target=sendMess, args=(sock, (localIP, 26951), session))
sendTHRD.start()


try:
	while session:
		bap = sock.recvfrom(4096)
		m = bap[0].decode("utf-8")
		print(m)
except KeyboardInterrupt:
	session = False
	sock.close()
	sendTHRD.abort()
