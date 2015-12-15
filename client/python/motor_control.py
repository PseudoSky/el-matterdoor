import sys
import subprocess
import time
import os
import signal

# from behavior import Behavior
from collections import deque
gestures = { "Wave_Left":["G0 Z100","G0 Z-100"],
          "Wave_Right":["G0 Z-100","G0 Z100"],
          "Spin_Left":["G0 X300 Y300 Z300"],
          "Spin_Right":["G0 X-300 Y-300 Z-300"],
          "Step_Left":["G0 X100 Y-100"],
          "Step_Right":["G0 X-100 Y100"],
          "Jump":["G0 X-300 Y300 Z-300","G0 X300 Y-300 Z300"],
          "Push":["G0 Y300 Z-300"],
          "Pull":["G0 Y-300 Z300"],
          "Kick_Left":["G0 X-100 Y-100","G0 X100 Y100"],
          "Kick_Right":["G0 X100 Y100","G0 X-100 Y-100"],
          "WalkForward":["G0 X600 Y300 Z100"],
          "WalkBackward":["G0 X-100 Y-300 Z-600"],
          "WalkAway":["G0 X 300","G0 X-300"],
          "Clap":["G0 Y100 Z100","G0 Y-100 Z-100"],
          "StandStill":["G0 X0 Y0 Z0"]}
class Behavior(object):
  """docstring for Behavior"""
  gestures={ "Wave_Left":["G0 Z100","G0 Z-100"],
          "Wave_Right":["G0 Z-100","G0 Z100"],
          "Spin_Left":["G0 X300 Y300 Z300"],
          "Spin_Right":["G0 X-300 Y-300 Z-300"],
          "Step_Left":["G0 X100 Y-100"],
          "Step_Right":["G0 X-100 Y100"],
          "Jump":["G0 X-300 Y300 Z-300","G0 X300 Y-300 Z300"],
          "Push":["G0 Y300 Z-300"],
          "Pull":["G0 Y-300 Z300"],
          "Kick_Left":["G0 X-100 Y-100","G0 X100 Y100"],
          "Kick_Right":["G0 X100 Y100","G0 X-100 Y-100"],
          "WalkForward":["G0 X600 Y300 Z100"],
          "WalkBackward":["G0 X-100 Y-300 Z-600"],
          "WalkAway":["G0 X 300","G0 X-300"],
          "Clap":["G0 Y100 Z100","G0 Y-100 Z-100"],
          "StandStill":["G0 X0 Y0 Z0"]}
  def __init__(self):
    super(Behavior, self).__init__()


    self.default_movement=['G0 X100 F300.944','G0 X120.000 F300.944']

    self.g_cue=deque()
    self.last_gesture=None

  def for_gesture(self,gesture_name):
    return self.gestures[gesture_name]

  def add_gesture(self, g):
    print "Adding In Behavior"
    # if((len(self.g_cue) == 0) or  (g["name"] != self.g_cue[-1])):
    print "Gesture "+g+" added to the queue."
    self.g_cue.append(g);


  def next(self):
    if len(self.g_cue)>0:
      print "Gcue"+ str(len(self.g_cue))
      self.last_gesture=self.g_cue.popleft()
      print self.last_gesture+str(self.gestures[self.last_gesture])
      return self.gestures[self.last_gesture]
    else:
      print "Default WRONG"+ str(len(self.g_cue))
      return self.default_movement


class MotorController:
  def __init__(self):
    self.proc = subprocess.Popen('python grbl_streamer.py',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
    self.behavior=Behavior()

    for i in range(10):
      self.proc.stdin.write('G0 X%.3f F300.944\n' % (10+i*10) )


  def add_gesture(self, g):
    print "Adding"
    self.behavior.g_cue.append(g["name"]);

  def move(self):
    # time.sleep(5)
    self.current_movement=self.behavior.next()
    print self.current_movement
    for cmd in self.current_movement:

      self.proc.stdin.write(cmd)
      print "Processed Command: "+cmd

  def run(self,g):
    # time.sleep(5)
    self.current_movement=gestures[g]
    print self.current_movement
    for cmd in self.current_movement:

      self.proc.stdin.write(cmd+"\n")
      # print "Processed Command: "+cmd


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

