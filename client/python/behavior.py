import sys
import subprocess
import time
import os
import signal


print 'One line at a time:'
proc = subprocess.Popen('python ../arduino/grbl_streamer.py',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
for i in range(10):
    proc.stdin.write('G0 X%.3f F300.944\n' % (10+i*10) )

try:
  while True:

    time.sleep(5)
    print "hey hey mama"
    proc.stdin.write('G0 X%3f F300.944\n' % Math.randInt(100))
    proc.stdin.write('G0 X120.000 F300.944\n')
    proc.stdin.write('is_running\n')

except KeyboardInterrupt:
    print "KILLLLLL"
    proc.stdin.write('kill\n')
    try:
      while True:
        next_line=proc.stdout.readline()
        if next_line=="Actually killed":
          print next_line
          break
    except KeyboardInterrupt:
      print "dbl"
    os.kill(proc.pid, signal.SIGUSR1)
