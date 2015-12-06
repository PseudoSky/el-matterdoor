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
    self.proc = subprocess.Popen('python ../arduino/grbl_streamer.py',
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
    print "KILLLLLL"
    self.proc.stdin.write('kill\n')
    try:
      while True:
        next_line=self.proc.stdout.readline()
        if next_line=="Actually killed":
          print next_line
          break
    except KeyboardInterrupt:
      print "dbl"
    os.kill(self.proc.pid, signal.SIGUSR1)


class NetworkListener:

  def __init__(self, mc):
    self.motor_control=mc
    self.ipAddresss = "128.237.171.97"#socket.gethostbyname(socket.gethostname())
    self.udpPort = 9001
    print("IP Address: ", self.ipAddresss)
    print("Port Number: ", self.udpPort)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind((self.ipAddresss, self.udpPort))

  def listen(self):
      try:
        while True:
          self.data, self.address = self.socket.recvfrom(2048)
          self.motor_control.add_gesture(json.loads(self.data))
          self.motor_control.run()

      except KeyboardInterrupt:
        self.motor_control.kill()

motor_control = MotorController()
networkListener = NetworkListener(motor_control)
networkListener.listen()
