from pynput import keyboard
from time import sleep
import threading



def on_press(key) :
    global endProgramme
    if key == keyboard.Key.esc:
        print("the end is commming......")
        endProgramme = True

def on_release(key) :
    global endProgramme
    if key == keyboard.Key.esc:
        endProgramme = True


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


while True :
    sleep(1)
exit()

app_is_running = True
def key_handler():
    while app_is_running:
        key = keyboard.read_key()
        if key == "W":
            print("W is pressed")
thread = threading.Thread(target=key_handler, daemon=True)
thread.start()
