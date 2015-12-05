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
    # output = proc.stdout.readline()
    # print output.rstrip()
# remainder = proc.communicate()[0]
# print remainder



# print
# print 'All output at once:'
# proc = subprocess.Popen('python ../arduino/grbl_streamer.py',
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         )
# for i in range(10):
#     proc.stdin.write('G1 X%.3f\n' % (i*100) )

# output = proc.communicate()[0]
# print "From main: "+output
# raw_input("  Press <Enter> to exit and disable grbl.")
# sys.stdin.readline()
try:
  while True:
    # next_line = sys.stdin.readline().strip()
    # if not (not next_line):
    #   print next_line
    # else:
    #   print "."

    # next_line=proc.stdout.readline()
    # if not (not next_line):
    #   print next_line

    time.sleep(5)
    print "hey hey mama"
    proc.stdin.write('G0 X100 F300.944\n' % Math.randInt(100))
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
