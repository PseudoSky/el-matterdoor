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

gestures = ['{"name" : "wave", "confidence" : ".2", "index" : "3"}',
            '{"name" : "jump", "confidence" : ".3", "index" : "4"}',
            '{"name" : "push", "confidence" : ".4", "index" : "5"}',
            '{"name" : "step_right", "confidence" : ".5", "index" : "6"}',]

for g in gestures:
    j = json.loads(g)
    print j['name'] # prints name of gesture
    print j['confidence'] #prints confidence level that that gesture is happening
    print j['index']
    name = j['name']
    confidence = j['confidence']
    index = j['index']
    