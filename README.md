# el-matterdoor

https://youtu.be/ymFxrqigQkQ

### Problem:
One of the revolutions in robotics is the ability to interact with responsive robots that translate human motion into robotic motion. This ability allows us to monitor physical motion in an environment and either mimic or augment that motion via robotic actions.

### Solution:
This system identifies gestures and creates corresponding electronic motor movements. The system then streams the Kinect gestures over UDP to the motor control system that queues the appropriate controls (Slight Latency Issues). The G-Code based motor controls are then pushed to an Arduino that controls the continuously spinning arms. I'd like to note that my team spent quite a bit of time designing these bearings from scratch. These bearings allow for circuitry to pass through the center without obstructing the bearings revolutions. Conventionally, these berryings are very expensive (more than 100$ per unit) because special components are needed to support the lateral forces that keep it from toppling. As you can see from the video linked below, our design supports rapid movements from the large wooden arms with minimal friction and lift without back driving our relatively small stepper motors.

Tools

* Development
  * Microsoft Kinect
  * Gesture Training and Recognition
  * Arduino, Grbl, G-Code
  * Lua, C++, NodeJS, Python
  * Express, Mongodb
  * Sketch3 (Architecture Diagram)
* Fabrication
  * Solidworks
  * OpenSCAD


## Install
Can't Remember ATM if you need to install sereal, if so
`pip install sereal`


## Start Network
`python client/network.py`

## Run Network & Motor Test
```
python client/network.py # Run network listener
python client/python/test.py #Run test
```
