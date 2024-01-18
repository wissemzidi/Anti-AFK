from pynput import keyboard
from time import sleep
import threading

KEYBOARD = keyboard.Controller() 




exit()

app_is_running = True
def key_handler():
    while app_is_running:
        key = keyboard.read_key()
        if key == "W":
            print("W is pressed")
thread = threading.Thread(target=key_handler, daemon=True)
thread.start()
