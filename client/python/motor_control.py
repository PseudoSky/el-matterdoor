import sys
import subprocess
import time
import os
import signal

from behavior import Behavior

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



  def move(self):
    # time.sleep(5)
    self.current_movement=self.behavior.next()
    for cmd in self.current_movement:
      self.proc.stdin.write(cmd)
      print "Processed Command: "+cmd


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

