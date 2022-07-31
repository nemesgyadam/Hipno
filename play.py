import vlc
import time
from config.default import config
from utils.parser import text2short
import os
clear = lambda: os.system('cls')
import tkinter as tk    
import threading
import time

pitch_rates = config['pitch_rates']
speed_rates = config['speed_rates']


def sound(sound):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(sound)
    player.set_media(media)
    player.play()
    time.sleep(0.5)
    duration = player.get_length() / 1000
    time.sleep(duration)
    

def keypress(event):
    if event.keysym == 'Escape':
        root.destroy()
    x = event.char
    global current
    global current_speed
    global current_pitch
    if x == "r":
        print ("Repeat")
        current-=1
    elif x == "q":
        try:
            current_pitch += 1
            print("Pitch increased to: " + str(pitch_rates[current_pitch]))
        except:
            print("Can't increase pitch")
            current_pitch -= 1
    elif x == "a":
        try:
            current_pitch -= 1
            print("Pitch decreased to: " + str(pitch_rates[current_pitch]))
        except:
            print("Can't decrease pitch")
            current_pitch += 1
    elif x == "w":
        try:
            current_speed += 1
            print("Speed increased to: " + str(speed_rates[current_speed]))
        except:
            print("Can't increase speed")
            current_speed-=1
    elif x == "s":
        try:
            current_speed -= 1
            print("Speed decreased to: " + str(speed_rates[current_speed]))
        except:
            print("Can't decrease speed")
            current_speed += 1
    else:
        print (f"Invalid keypress:{x}")
        
def control_thread():
    root = tk.Tk()
    root.bind_all('<Key>', keypress)
    root.withdraw()
    root.mainloop()

current_pitch = 3
current_speed = 7
current = 0
print("Use it well...")
print()
print()
print("Controls:")
print("r: repeat")
print("q: increase pitch")
print("a: decrease pitch")
print("w: increase speed")
print("s: decrease speed")
time.sleep(3)


x = threading.Thread(target=control_thread)
x.start()

while current != len(config['texts']):
    clear()
    _text = config['texts'][current]
    _next = config['texts'][current+1]
    print(_text)
    print(f"Next: {_next}")
    sound(f"resources/{text2short(_text)}p{pitch_rates[current_pitch]}_s{speed_rates[current_speed]}.mp3")
  
    current +=1
    
x.join()
print("Done")
