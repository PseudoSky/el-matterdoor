import json

import socket

UDP_IP = socket.gethostbyname(socket.gethostname())
print("IP Address: " + UDP_IP)
UDP_PORT = 9001
print("UDP Socket = " + str(UDP_PORT))
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSocket.bind((UDP_IP, UDP_PORT))


while(True):
    data, addr = UDPSocket.recvfrom(1024)
    print ("received message: ", data)
    j = json.loads(data)
    print j['name'] # prints name of gesture
    print j['confidence'] #prints confidence level that that gesture is happening