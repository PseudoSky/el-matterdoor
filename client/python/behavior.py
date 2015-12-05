import json

gestures = ['{"name" : "wave_right", "confidence" : ".2", "index" : "1"}',
            '{"name" : "step_left", "confidence" : ".3", "index" : "2"}',
            '{"name" : "step_right", "confidence" : ".4", "index" : "3"}',
            '{"name" : "standstill", "confidence" : ".5", "index" : "4"}',
            '{"name" : "push", "confidence" : ".6", "index" : "5"}',
            '{"name" : "pull", "confidence" : ".7", "index" : "6"}',
            '{"name" : "jump", "confidence" : ".8", "index" : "7"}',
            '{"name" : "kick_left", "confidence" : ".9", "index" : "8"}',
            '{"name" : "kick_right", "confidence" : ".1", "index" : "9"}',
            '{"name" : "spin_left", "confidence" : ".2", "index" : "10"}',
            '{"name" : "spin_right", "confidence" : ".3", "index" : "11"}',
            '{"name" : "walkforward", "confidence" : ".4", "index" : "12"}',
            '{"name" : "walkbackward", "confidence" : ".5", "index" : "13"}',
            '{"name" : "walkaway", "confidence" : ".6", "index" : "14"}',
            '{"name" : "wave_left", "confidence" : ".7", "index" : "15"}',
            '{"name" : "clap", "confidence" : ".5", "index" : "16"}',]

for g in gestures:
    j = json.loads(g)
    print j['name'] # prints name of gesture
    print j['confidence'] #prints confidence level that that gesture is happening
    print j['index']
    name = j['name']
    confidence = j['confidence']
    index = j['index']
    if name == "jump":
        print "                                        hi!"
    if confidence == ".2":
        print "                                         heyy"
    if index == "3":
        print "                                         yoo"