import socket
import json
import sys
import subprocess
import time
import os
import signal

gestureCues = []

class MotorController:
  def __init__(self):
    self.proc = subprocess.Popen('python client/arduino/grbl_streamer.py',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
    self.g_cue=[]

    for i in range(10):
      self.proc.stdin.write('G0 X%.3f F300.944\n' % (10+i*10) )

  def add_gesture(self, g):
    print g
    if((len(self.g_cue) == 0) or (g["name"] != self.g_cue[-1]["name"])):
      self.g_cue.append(g);

  def run(self):
    time.sleep(5)
    print "hey hey mama"
    self.proc.stdin.write('G0 X100 F300.944\n')
    self.proc.stdin.write('G0 X120.000 F300.944\n')
    self.proc.stdin.write('is_running\n')

  def kill(self):
    print "\n\n"+("*"*50)
    print "\nAttempting to Kill Motor Control..."
    self.proc.stdin.write('kill\n')
    self.proc.terminate()
    print "\nKill Signal Sent..."

    try:
      while self.proc.poll():
        # if not self.proc.returncode:

        next_line=self.proc.stdout.readline()
        if next_line=="Actually killed":
          print next_line
          break
        next_line=self.proc.stderr.readline()
        if next_line=="Actually killed":
          print next_line
          break
        else:
          print "\nProcess Successfully Terminated..."
          print "\n\n"+("*"*50)
          return 1
      print "\nSub Process Successfully Terminated"
      print "\n"+("*"*50)
      return 1
    except KeyboardInterrupt:
      print "\n"+("*"*50)
      print "\nForce Killing Motor Control..."

      self.proc.kill()


class NetworkListener:

  def __init__(self, mc):
    self.motor_control=mc

    # On school network, this function doesn't work
    self.get_ip()
    self.udp_port = 9001
    print("IP Address: ", self.ip)
    print("Port Number: ", self.udp_port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind((self.ip, self.udp_port))

    self.listen()



  def get_ip(self):
    try:
      self.ip = socket.gethostbyname(socket.gethostname())
    except Exception:
      self.ip = "127.0.0.1"

  def listen(self):
      try:
        while True:
          self.data, self.address = self.socket.recvfrom(2048)
          self.motor_control.add_gesture(json.loads(self.data))
          self.motor_control.run()

      except KeyboardInterrupt:
        self.motor_control.kill()
        print "\nClosing Main Thread..."
        print "\n"+("*"*50)
        print "\nGoodbye"

motor_control = MotorController()
networkListener = NetworkListener(motor_control)
