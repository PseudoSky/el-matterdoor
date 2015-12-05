import socket
import json

gestureCues = []

class NetworkListener:

	def __init__(self):
		self.ipAddresss = socket.gethostbyname(socket.gethostname())
		self.udpPort = 9001
		print("IP Address: ", self.ipAddresss)
		print("Port Number: ", self.udpPort)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind((self.ipAddresss, self.udpPort))

	def listen(self):
		while True:
			self.data, self.address = self.socket.recvfrom(2048)
			self.currentGesture = json.loads(self.data)
			if((len(gestureCues) == 0) or (self.currentGesture["name"] != gestureCues[-1]["name"])):
				gestureCues.append(self.currentGesture)
			print gestureCues

networkListener = NetworkListener()
networkListener.listen()
