from collections import deque

class Behavior(object):
  """docstring for Behavior"""
  gestures={ "Wave_Left":["G0 Z30","G0 Z-30","G0 Z0"],
      "Wave_Right":["G0 Z-100","G0 Z100"],
      "Spin_Left":["G0 X300 Y300 Z300"],
      "Spin_Right":["G0 X-300 Y-300 Z-300"],
      "Step_Left":["G0 X100 Y-100"],
      "Step_Right":["G0 X-100 Y100"],
      "Jump":["G0 X-300 Y300 Z-300","G0 X300 Y-300 Z300"],
      "Push":["G0 Y-300 Z300"],
      "Pull":["G0 Y-300 Z300"],
      "Kick_Left":["G0 X-100 Y-100","G0 X100 Y100"],
      "Kick_Right":["G0 X100 Y100","G0 X-100 Y-100"],
      "WalkForward":["G0 X600 Y300 Z100"],
      "WalkBackward":["G0 X-100 Y-300 Z-600"],
      "WalkAway":["G0 X 300","G0 X-300"],
      "Clap":["G0 Y100 Z100","G0 Y-100 Z-100"],
      "StandStill":["G0 X0 Y0 Z0"]}

  def __init__(self):
    super(Behavior, self).__init__()


    self.default_movement=['G0 X100','G0 X0.000']

    self.g_cue=deque()
    self.last_gesture=None

  def for_gesture(self,gesture_name):
    return self.gestures[gesture_name]

  def add_gesture(self, g):
    print "Adding In Behavior"
    # if((len(self.g_cue) == 0) or  (g["name"] != self.g_cue[-1])):
    if(g["cmd"]):
      self.line_count+=1
      g["name"]=str(self.line_count)
      self.Gestures[g["name"]]=g["cmd"]
      print 'Adding gcode cmd: '+g["cmd"]
    print "Gesture "+g+" added to the queue."
    self.g_cue.append(g["name"]);


  def next(self):
    if len(self.g_cue)>0:
      print "Gcue"+ str(len(self.g_cue))
      return self.gestures[self.g_cue.popleft()]
    else:
      print "Default WRONG"+ str(len(self.g_cue))
      return self.default_movement
