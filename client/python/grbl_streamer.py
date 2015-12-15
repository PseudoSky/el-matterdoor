#!/usr/bin/env python
"""\
    Simple g-code streaming script for grbl

    Provided as an illustration of the basic communication interface
    for grbl. When grbl has finished parsing the g-code block, it will
    return an 'ok' or 'error' response. When the planner buffer is full,
    grbl will not send a response until the planner buffer clears space.

    G02/03 arcs are special exceptions, where they inject short line
    segments directly into the planner. So there may not be a response
    from grbl for the duration of the arc.

    ---------------------
    The MIT License (MIT)

    Copyright (c) 2012 Sungeun K. Jeon

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    ---------------------
    """

import serial
import time
import subprocess
import sys
import re
import serial.tools.list_ports
RX_BUFFER_SIZE = 128
verbose=True
is_running=False

class Grbl(object):

    def __init__(self):
        self.serial_port = '/dev/tty.usbmodem1451'
        for p in serial.tools.list_ports.comports():
            if 'usbmodem' in p[0]:
                self.serial_port=p[0].replace('cu','tty')
                print self.serial_port
        self.s = serial.Serial(self.serial_port,115200)
        # sys.stderr.write('grbl_streamer.py: starting\n')
        print 'grbl_streamer.py: starting\n'
        # sys.stderr.flush()

        try:

            # Wake up grbl
            self.s.write("\r\n\r\n")
            time.sleep(2)   # Wait for grbl to initialize
            self.s.flushInput()  # Flush startup text in serial input
            count=0
            # run_gcode(['G21 G90 G17 G94 G54','G0 X0.000'])
            cmd_buffer=[]
            while True:

                next_line = sys.stdin.readline().strip()

                if "kill" in next_line:
                    self.s.close()
                    sys.stderr.write("Actually killed\n")
                    # print "Actually killed"
                    break
                elif "is_running" in next_line:
                    # sys.stderr.write(is_running and "Is Running" or "Is Not Running")
                    print is_running and "Is Running" or "Is Not Running"

                else:
                    # sys.stderr.write( next_line)
                    output=self.run_gcode([next_line])

        except KeyboardInterrupt:
            print "\n\n"+("*"*50)
            print "\nKilling Motor Control And Closing Connection..."
            self.s.close()
            print "\nConnection Closed"
            print "\n"+("*"*50)
            print "\n\nGoodbye"

        self.s.close()



    # Stream g-code to grbl


    def pp(s):
        print self.s+""
        # sys.stdout.write(s+'\n')

        return 1


    def run_gcode(self, commands):

        # print f
        print commands[0]
        l_count=0
        g_count = 0
        c_line = []
        scon=self.s
        # for s_conn in serial_connections:
        for line in commands:
            l_count += 1 # Iterate line counter
            l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize

            l_block = line.strip()
            c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
            grbl_out = ''

            # While the arduino buffer is too full to accept the next command, wait
            while sum(c_line) >= RX_BUFFER_SIZE-1 | self.s.inWaiting() :
                out_temp = self.s.readline().strip() # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                    print "  Debug: ",out_temp # Debug response
                else :
                    grbl_out += out_temp;
                    g_count += 1 # Iterate g-code counter
                    grbl_out += str(g_count); # Add line finished indicator
                    del c_line[0] # Delete the block character count corresponding to the last 'ok'
            # Then write the command


            if verbose: print "SND: " + str(l_count) + " : " + l_block,
            self.s.write(l_block + '\n') # Send g-code block to grbl
            if verbose : print "BUF:",str(sum(c_line)),"REC:",grbl_out


Grbl()
