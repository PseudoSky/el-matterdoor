import socket
import json

testures = ['{"name" : "wave", "confidence" : ".2", "index" : "3"}',
            '{"name" : "jump", "confidence" : ".3", "index" : "4"}',
            '{"name" : "push", "confidence" : ".4", "index" : "5"}',
            '{"name" : "step_right", "confidence" : ".5", "index" : "6"}']

class NetworkTest:

  def __init__(self):
    # On school network, this function doesn't work
    self.get_ip()
    self.udpPort = 9002
    print("IP Address: ", self.ip)
    print("Port Number: ", self.udpPort)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind((self.ip, self.udpPort))

  def get_ip(self):
    try:
      self.ip = socket.gethostbyname(socket.gethostname())
    except Exception:
      self.ip = "127.0.0.1"


  def listen(self):
    for gest in testures:
      # self.data, self.address = self.socket.recvfrom(2048)
      print gest
      self.socket.sendto(gest, (self.ip, 9001))


networkListener = NetworkTest()
networkListener.listen()
