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

	def __init__(self,interactive=False):
		self.interactive = interactive
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
			while True and not(self.interactive):

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

		# self.go=go
		# if(not(self.interactive)):
		# self.s.close()



	# Stream g-code to grbl


	def pp(s):
		print self.s+""
		# sys.stdout.write(s+'\n')

		return 1

	def go(self, commands):

		# print f
		if not(type(commands)==type([])):
			commands=[commands]

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
	def home(self):
		self.go('G0 X0 Y0')
		print "Homed"

	def toggle(self):
		if self.s.isOpen():
			self.s.close()
			print "Connection Closed"
		else:
			self.s.open()
			print "Connection Open"

	def validate(self, cmds, bounds):
		summary=[0,0,0]
		ranges={"maxs":[0,0,0],"mins":[1000,1000,1000]}
		for i in range(len(cmds)):
			g=cmds[i]
			if 'x' in bounds:
				if g[1]>bounds['x']:
					print "X Bounds Error (line "+str(i)+": "+str(g)
					summary[0]+=1
				if g[1]>ranges["maxs"][0]:ranges["maxs"][0]=g[1]
				if g[1]<ranges["mins"][0] and g[1]>0 :ranges["mins"][0]=g[1]
			if 'y' in bounds:
				if g[2]>bounds['y']:
					print "Y Bounds Error (line "+str(i)+": "+str(g)
					summary[1]+=1
				if g[2]>ranges["maxs"][1]:ranges["maxs"][1]=g[2]
				if g[2]<ranges["mins"][1] and g[2]>0 :ranges["mins"][1]=g[2]
			if 'z' in bounds:
				if g[3]>bounds['z']:
					print "Z Bounds Error (line "+str(i)+": "+str(g)
					summary[2]+=1
				if g[3]>ranges["maxs"][2]:ranges["maxs"][2]=g[3]
				if g[3]<ranges["mins"][2] and g[3]>0 :ranges["mins"][2]=g[3]
		print "\nBound Error Summary"
		print "\tX : "+str(summary[0])
		print "\tY : "+str(summary[1])
		print "\tZ : "+str(summary[2])

		print "\nRange Summary"
		print "\tX\tmax:{:.3f}\tmin:{:.3f}".format(ranges["maxs"][0],ranges["mins"][0])
		print "\tY\tmax:{:.3f}\tmin:{:.3f}".format(ranges["maxs"][1],ranges["mins"][1])
		print "\tZ\tmax:{:.3f}\tmin:{:.3f}".format(ranges["maxs"][2],ranges["mins"][2])

		print "\nOptimal Scale"
		if ranges["maxs"][0]>0: print "\tX scalar:\t{:.3f}".format(bounds['x']/ranges["maxs"][0])
		if ranges["maxs"][1]>0: print "\tY scalar:\t{:.3f}".format(bounds['y']/ranges["maxs"][1])
		if ranges["maxs"][2]>0: print "\tZ scalar:\t{:.3f}".format(bounds['z']/ranges["maxs"][2])


	# parse_file
	# 
	#		 inp:
	#				Takes a gcode path or 
	#				Gcode cmds in an array
	#		 
	#		 scalars:
	#				Float multiples to scale dimensions
	#		 
	#		 bounds:
	#				object definind the upper dimensional bounds 
	def parse(self, inp, scalars=[1.0,1.0,1.0], bounds={}):
		if type(inp) == type(""): inp = open(inp, 'r+')
		cmds=[]
		for line in inp:
			cmd=line.split()
			cmd=[cmd[0],float(cmd[1][1:]),float(cmd[2][1:])]
			cmd[0]='G0'
			if len(cmd)>1 and len(str(cmd[1]))>0: cmd[1]=cmd[1]*scalars[0]
			if len(cmd)>2 and len(str(cmd[2]))>0: cmd[2]=cmd[2]*scalars[1]
			if len(cmd)>3 and len(str(cmd[3]))>0: cmd[3]=cmd[3]*scalars[2]
			cmds.append(cmd)
		if type(inp) != type([]):
			inp.close()
		if len(bounds)>0:
			self.validate(cmds,bounds)
		return cmds

	# g=Grbl(True)
	# path="/Users/snow/Desktop/chewbacca.gcode"
	# d=g.format(path,[.125,.245],{"x":400,"y":200})
	def format(self, cmds, scalars=[1.0,1.0,1.0], bounds={}):
		if type(cmds) == type(""): cmds=self.parse(cmds,scalars,bounds)
		formatted=[]
		for cmd in cmds:
			clean='G0'
			if len(cmd)>1 and len(str(cmd[1]))>0: clean+=' X'+'{:.3f}'.format(cmd[1])
			if len(cmd)>2 and len(str(cmd[2]))>0: clean+=' Y'+'{:.3f}'.format(cmd[2])
			if len(cmd)>3 and len(str(cmd[3]))>0: clean+=' Z'+'{:.3f}'.format(cmd[3])
			formatted.append(clean)
		return formatted

	def file(path):
		f = open(path, 'r+')
		for line in f:
			self.go(line)

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

# return Grbl
# gr=Grbl(True)
