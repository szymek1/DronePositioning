import socket

localIP     = "192.168.43.181"
localPort   = 26950
bufferSize  = 4096

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# UDPServerSocket.bind((localIP, localPort))

print("listening")
response = bytes("1", encoding="utf-8")



while(True):

    # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    # message = bytesAddressPair[0].decode('utf-8')

    # print(message)

    UDPServerSocket.sendto(response, (localIP, 26951))


