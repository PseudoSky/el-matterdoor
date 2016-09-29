import sys
import subprocess
import time
import os
import signal

# from behavior import Behavior
from collections import deque
gestures = { "Wave_Left":["G0 X100 Y100 Z20","G0 Z-20"],
          "Wave_Right":["G0 Z-10","G0 Z10"],
          "Spin_Left":["G0 X30 Y30 Z30"],
          "Spin_Right":["G0 X-30 Y-30 Z-30"],
          "Step_Left":["G0 X10 Y-10"],
          "Step_Right":["G0 X-10 Y10 Z100"],
          "Jump":["G0 X-30 Y30 Z-30","G0 X30 Y-30 Z30"],
          "Push":["G0 X10 Y30 Z-30"],
          "Pull":["G0 X-10 Y-30 Z30"],
          "Kick_Left":["G0 X-10 Y-10","G0 X10 Y10"],
          "Kick_Right":["G0 X10 Y10","G0 X-10 Y-10"],
          "WalkForward":["G0 X60 Y30 Z10"],
          "WalkBackward":["G0 X-10 Y-30 Z-60"],
          "WalkAway":["G0 X30 Z10","G0 X-30 Z10"],
          "Clap":["G0 Y10 Z10","G0 Y-10 Z-10"],
          "StandStill":["G0 X1 Y-1 Z5"]}
import random
class Behavior(object):
  """docstring for Behavior"""
  gestures={ "Wave_Left":["G0 X100 Y100 Z20","G0 Z-20"],
          "Wave_Right":["G0 Z-10","G0 Z10"],
          "Spin_Left":["G0 X30 Y30 Z30"],
          "Spin_Right":["G0 X-30 Y-30 Z-30"],
          "Step_Left":["G0 X10 Y-10"],
          "Step_Right":["G0 X-10 Y10 Z100"],
          "Jump":["G0 X-30 Y30 Z-30","G0 X30 Y-30 Z30"],
          "Push":["G0 X10 Y30 Z-30"],
          "Pull":["G0 X-10 Y-30 Z30"],
          "Kick_Left":["G0 X-10 Y-10","G0 X10 Y10"],
          "Kick_Right":["G0 X10 Y10","G0 X-10 Y-10"],
          "WalkForward":["G0 X60 Y30 Z10"],
          "WalkBackward":["G0 X-10 Y-30 Z-60"],
          "WalkAway":["G0 X30 Z10","G0 X-30 Z10"],
          "Clap":["G0 Y10 Z10","G0 Y-10 Z-10"],
          "StandStill":[""]}
  line_count=0
  def __init__(self):
    super(Behavior, self).__init__()


    self.default_movement=['G0 X10 F30.944','G0 X12.000 F30.944']

    self.g_cue=deque()
    self.last_gesture=None

  def for_gesture(self,gesture_name):
    return self.gestures[gesture_name]

  def add_gesture(self, g):
    print "Adding In Behavior"
    # if((len(self.g_cue) == 0) or  (g["name"] != self.g_cue[-1])):
    print "Gesture "+str(g)+" added to the queue."
    if "cmd" in g:
      self.line_count+=1
      g["name"]=str(self.line_count)
      print str(g)
      self.gestures[g["name"]]=[g["cmd"]]
      print 'Adding gcode cmd: '+str(self.gestures[g["name"]]) +' should = '+str(g["cmd"])
    if g!= "StandStill":
      self.g_cue.append(g);


  def next(self):
    if len(self.g_cue)>0:
      
      self.last_gesture=self.g_cue.popleft()
      print "Loading From Gcue"+str(self.gestures[self.last_gesture])
      # print self.last_gesture+str(self.gestures[self.last_gesture])
      return self.gestures[self.last_gesture]
    else:
      print "Nothing To Do"
      # return random.choice(self.gestures.values())


class MotorController:
  def __init__(self):
    self.proc = subprocess.Popen('python `pwd`/client/python/grbl_streamer.py',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
    self.behavior=Behavior()

    for i in range(10):
      self.proc.stdin.write('G0 X%.3f F30.944\n' % (10+i*10) )


  def add_gesture(self, g):
    print "Adding"
    if "cmd" in g or g["name"]!="StandStill":
      self.behavior.add_gesture(g)
      # self.behavior.g_cue.append(g["name"]);

  def move(self):
    # time.sleep(5)
    self.current_movement=self.behavior.next()
    print self.current_movement
    for cmd in self.current_movement:

      self.proc.stdin.write(cmd+"\n")
      print "Move From Queue: "+cmd

    return self.current_movement
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

