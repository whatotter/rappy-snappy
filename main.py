import os
import time
import keyboard
import pytoml as toml
import icon

if "keys.toml" not in os.listdir("./"):
    with open("keys.toml", "w") as f:
        # is this smart? probably not
        f.write("keys = [\"a\",\"d\"]\npollingRate = 100 # miliseconds")
        f.flush()

config = toml.load(open("./keys.toml", "r"))
keys = config["keys"]
polling = int(config["pollingRate"])/1000

keyLog = {} # wow that's a bad name
keyQueue = []

def kbPress(ev:keyboard.KeyboardEvent):
    if ev.name not in keyLog:
        keyLog[ev.name] = ev.time

def kbRelease(ev:keyboard.KeyboardEvent):
    if ev.name in keyLog:
        keyLog.pop(ev.name)
    
    if ev.name in keyQueue:
        keyQueue.remove(ev.name)

if __name__ == "__main__":
    for key in keys: # check over every key
        keyboard.on_press_key(key, kbPress)
        keyboard.on_release_key(key, kbRelease)

    print("[+] running on keys: {}".format(keys))
    icon.setupIcon(config)

    while True:

        if len(keyLog) >= 2: # if 2 or more keys are simultaneously pressed

            # find the first/earliest key that was pressed
            earliestKey = None
            earliestTs = 9e9
            for key in keyLog:
                timestamp = keyLog[key]

                if earliestTs > timestamp:
                    earliestTs = timestamp
                    earliestKey = key

            # release that key from the keyboard
            keyLog.pop(earliestKey)
            keyboard.release(earliestKey)

            # add it to our queue, to be pressed once we've let go of all keys
            if earliestKey not in keyQueue:
                keyQueue.append(earliestKey)

            print("[+] released {}".format(earliestKey))
        
        if len(keyLog) == 0 and len(keyQueue) != 0: # we've let go of all keys, and a key is waiting to be pressed down
            # simulate the key being held down
            keyboard.press(keyQueue[0])
            keyLog[keyQueue[0]] = time.time()

            print("[+] pressed {}".format(keyQueue[0]))
            keyQueue.pop(0)


        time.sleep(polling)