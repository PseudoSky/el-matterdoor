import socket
import json

testures = ['{"name" : "wave", "confidence" : ".2", "index" : "3"}',
            '{"name" : "jump", "confidence" : ".3", "index" : "4"}',
            '{"name" : "push", "confidence" : ".4", "index" : "5"}',
            '{"name" : "step_right", "confidence" : ".5", "index" : "6"}']

class NetworkListener:

	def __init__(self):
		self.ipAddresss = "128.237.171.97" #socket.gethostbyname(socket.gethostname())
		self.udpPort = 9002
		print("IP Address: ", self.ipAddresss)
		print("Port Number: ", self.udpPort)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind((self.ipAddresss, self.udpPort))

	def listen(self):
		for gest in testures:
			# self.data, self.address = self.socket.recvfrom(2048)
			print gest
			self.socket.sendto(gest, (self.ipAddresss, 9001))


networkListener = NetworkListener()
networkListener.listen()
