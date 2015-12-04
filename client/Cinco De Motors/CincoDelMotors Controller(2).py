import serial
import serial.tools.list_ports

class CincoDelMotors:     
 
    def __init__(self):
        availablePorts = list(serial.tools.list_ports.comports())   
        self.arduinos = []
        for x in range(len(availablePorts)):
            self.arduinos.append(serial.Serial(availablePorts[x][0]))

    def printThings(self):
        print self.arduinos

cincoDelMotors = CincoDelMotors()
cincoDelMotors.printThings()
