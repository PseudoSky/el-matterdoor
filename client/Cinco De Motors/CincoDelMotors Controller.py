import serial
import serial.tools.list_ports

availablePorts = list(serial.tools.list_ports.comports())   
arduinos = []
for x in range(len(availablePorts)):
    arduinos.append(serial.Serial(availablePorts[x][0]))
