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
    for numChar in range(len(data)):
        print("Char" , numChar, ": " + chr(data[numChar]))
        gestureNum = chr(data[0])
