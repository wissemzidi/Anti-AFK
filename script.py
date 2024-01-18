from PyQt5.QtWidgets import QApplication
from pynput import keyboard, mouse
from PyQt5.QtGui import QIcon
from threading import Thread
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from os import _exit, path
from random import randint
import win32api, win32con
from time import sleep
import pyautogui
import json


def main() :
    """
    choose mouse or keyboard 
    probability keyboard=0.9, mouse=0.1
    """
    global mainThread
    time = win.timeInput.text()
    if time == "" :
        time = 86400    # equivalent to 1 day
    elif not time.isdigit() :
        win.error.setText("This number isn't valid !")
        return
    else :
        time = int(time)
    mainThread = Thread(target=loopThread, args=[time], daemon=True)
    mainThread.start()


def stopMain() :
    global endProgramme
    endProgramme = True
    win.timeLeft.setText("STOPED")
    return


def loopThread(time) :
    global endProgramme
    mouseLeftAlowed = win.mouseLeft.isChecked()
    mouseRightAlowed = win.mouseRight.isChecked()
    mouseMoveAlowed = win.mouseMovement.isChecked()
    sleep(1)
    while not endProgramme and time > 0 :
        randKeyboard()
        randMouse(mouseLeftAlowed, mouseRightAlowed, mouseMoveAlowed)
        sleepTime = randint(0, 10) / 100
        sleep(sleepTime)
        if time :
            time -= sleepTime
        win.timeLeft.setText("Time Left : "+str(int(time))+"s")
    if win.autoExit.isChecked():
        _exit(0)
    win.timeLeft.setText("STOPED")
    endProgramme = False


def randMouse(mouseLeftAlowed, mouseRightAlowed, mouseMoveAlowed) :
    r = randint(0, 10)
    if mouseLeftAlowed and r in [0, 1, 2] :
        print("left click !")
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        sleep(.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # pyautogui.leftClick(duration=0.2, interval=0.1)
    if mouseRightAlowed and r == 9:
        print("right click !")
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        sleep(.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        # pyautogui.leftClick(duration=0.2, interval=0.1)
    if mouseMoveAlowed and r in [1, 2, 3, 4, 5, 6, 7, 8] :
        screen = App.primaryScreen()
        size = screen.size()
        w, h = size.width(), size.height()
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, randint(20, w // 2), randint(20, h // 2), 0, 0)

def randKeyboard():
    if len(alowedMoves) == 0 :
        return
    
    r = randint(0, len(alowedMoves) - 1)
    pressKey(alowedMoves[r], randint(0, 500) / 100)

def pressKey(key, duration):
    pyautogui.keyDown(key)
    sleep(duration)
    pyautogui.keyUp(key)
    return


def on_press(key) :
    global endProgramme
    if key == keyboard.Key.esc:
        endProgramme = True
    elif key == keyboard.Key.f1:
        endProgramme = False
        main()


def initWin(winTitle):
    """
    Initializes the win object with the specified win title.

    Parameters:
        winTitle (str): The title to set for the win window.

    Returns:
        None
    """
    win.setWindowTitle(winTitle)
    win.setWindowIcon(QIcon('./ui/icon.png'))
    win.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
    # win.setAttribute(Qt.WA_TranslucentBackground)

    # rendering Images
    # win.exitBtn.setIcon(QIcon(":/exit/exit.png"))
    # win.exitBtn.setText("")

    # handling events
    win.setMouseTracking(True)
    win.header.mouseReleaseEvent = mouseReleaseEvent
    win.header.mousePressEvent = mousePressEvent
    win.header.mouseMoveEvent = mouseMoveEvent

    # move the Window to top 
    # topLeftPoint = QApplication.desktop().availableGeometry().topLeft()
    # win.move(topLeftPoint)

    getAlowedMoves()
    setAlowedMovesInUi()



def setAlowedMovesInUi() :
    for carac in allKeysList :
        getattr(win, carac+"Btn").setChecked(False)
    for carac in alowedMoves :
        getattr(win, carac+"Btn").setChecked(True)


def getAlowedMoves() :
    global alowedMoves
    if path.exists("./config/config.json"):
        try:
            with open("./config/config.json", "r") as f :
                data = json.loads(f.read())
                if len(data["moves"]) != "0":
                    alowedMoves = data["moves"]
        except Exception:
            pass


def saveKeys(moves, setToUi) :
    global alowedMoves
    alowedMoves = moves
    data = {}
    data["moves"] = moves
    with open("./config/config.json", "w") as f :
        f.write(json.dumps(data))
    if setToUi :
        setAlowedMovesInUi()


def changeAlowedKeys() :
    global alowedMoves
    alowedMoves = []
    for key in allKeysList :
        if (getattr(win, key+"Btn").isChecked()) :
            alowedMoves.append(key)
    saveKeys(alowedMoves, False)


def mousePressEvent(event):
    win._old_pos = event.pos()
def mouseReleaseEvent(event):
    win._old_pos = None
def mouseMoveEvent(event):
    try:
        if not win._old_pos:
            return
        delta = event.pos() - win._old_pos
        win.move(win.pos() + delta)
    except :
        pass


def minimize():
    """
    Minimizes the window by calling the showMinimized() method of the `win` object.
    """
    win.showMinimized()



endProgramme = False
KEYBOARD = keyboard.Controller()
MOUSE = mouse.Controller()
listener = keyboard.Listener(on_press=on_press)
listener.start()

App = QApplication([])
win = loadUi("./ui/main.ui")

alowedMoves = ["Z", "Q", "S", "D", "Space"]
allKeysList = ["Z", "Q", "S", "D", "Space", "W", "A"]
initWin(winTitle="Anti AFK")

for carac in allKeysList:
    getattr(win, carac+"Btn").stateChanged.connect(changeAlowedKeys)

mainThread = None

win.startBtn.clicked.connect(main)
win.stopBtn.clicked.connect(stopMain)
win.startWithoutTimerBtn.clicked.connect(main)
win.minimizeBtn.clicked.connect(minimize)
win.exitBtn.clicked.connect(_exit)

win.azertyPreset.clicked.connect(lambda: saveKeys(["Z", "Q", "S", "D", "Space"], True))
win.qwertyPreset.clicked.connect(lambda: saveKeys(["W", "A", "S", "D", "Space"], True))
win.resetPreset.clicked.connect(lambda: saveKeys([], True))

win.show()
App.exec()
