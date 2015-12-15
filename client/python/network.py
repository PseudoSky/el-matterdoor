import socket
import json


from motor_control import MotorController

class NetworkListener:

  def __init__(self):
    self.motor_control=MotorController()

    # On school network, this function doesn't work
    self.get_ip()
    self.udp_port = 9001

    success=False
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in [0,7,13,17]:
      try:
        self.udp_port+=i
        self.socket.bind((self.ip, self.udp_port))
        print "\n"+("*"*50)
        print "\nBound To {}:{}\n".format(self.ip,self.udp_port)
        print("IP Address: ", self.ip)
        print("Port Number: ", self.udp_port)
        print ("*"*50)+"\n"
        success=True
        break
      except Exception:
        print "Failed To Bind Port: {}".format(self.udp_port)
        self.udp_port-=i
    if not success:
      print "\n"+("*"*50)
      print "\n"+("*"*15)+" UDP FAILED TO BIND "+("*"*15)
      print ("*"*50)

    self.listen()



  def get_ip(self):
    try:
      self.ip = socket.gethostbyname(socket.gethostname())
    except Exception:
      print "\n"+("*"*50)
      print ("*"*12)+" Forced To Use 127.0.0.1 "+("*"*13)
      print ("*"*50)+"\n"
      self.ip = "127.0.0.1"

  def listen(self):
      try:
        while True:
          self.data, self.address = self.socket.recvfrom(2048)

          try:
            movement=json.loads(self.data)
            self.motor_control.run(movement["name"])
            # self.motor_control.add_gesture()

          except Exception:
            print "\nPacket Recieved: \n"+self.data

          # self.motor_control.move()

      except KeyboardInterrupt:
        self.motor_control.kill()
        print "\nClosing Main Thread..."
        print "\n"+("*"*50)
        print "\nGoodbye"

NetworkListener()