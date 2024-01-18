from PyQt5.QtWidgets import QApplication
from pynput import keyboard, mouse
from PyQt5.QtGui import QIcon
from threading import Thread
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from random import randint
from time import sleep
from os import _exit
import json

KEYBOARD = keyboard.Controller()
MOUSE = mouse.Controller()

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
    return


def loopThread(time) :
    global endProgramme
    while not endProgramme and time > 0 :
        if randint(0, 10) :
            randKeyboard()
        else :
            randMouse()
        sleepTime = randint(0, 10) / 100
        sleep(sleepTime)
        if time :
            time -= sleepTime
        win.timeLeft.setText("Time Left : "+str(int(time))+"s")
    if win.autoExit.isChecked():
        _exit(0)
    endProgramme = False


def randMouse() :
    screen = App.primaryScreen()
    size = screen.size()
    h, v = size.width(), size.height()
    if randint(0, 10) :
        # MOUSE.move(randint(0, h), randint(0, v))
        MOUSE.click(mouse.Button.left)
    else :
        # MOUSE.move(randint(0, h), randint(0, v))
        MOUSE.click(mouse.Button.right)

def randKeyboard():
    r = randint(0, len(alowedMoves) - 1)
    for i in range(randint(1, 20)) :
        if alowedMoves[r] == "Space" :
            KEYBOARD.press(keyboard.Key.space)
        else :
            KEYBOARD.press(alowedMoves[r])


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
    win.setWindowFlags(Qt.FramelessWindowHint)
    # win.setAttribute(Qt.WA_TranslucentBackground)

    # rendering Images
    win.exitBtn.setIcon(QIcon(":/exit/exit.png"))
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
    with open("./config/config.json", "r") as f :
        data = json.loads(f.read())
        if len(data["moves"]) != "0":
            alowedMoves = data["moves"]


def saveMoves(moves) :
    global alowedMoves
    alowedMoves = moves
    data = {}
    data["moves"] = moves
    with open("./config/config.json", "w") as f :
        f.write(json.dumps(data))
    setAlowedMovesInUi()


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
listener = keyboard.Listener(on_press=on_press)
listener.start()

App = QApplication([])
win = loadUi("./ui/main.ui")

alowedMoves = ["Z", "Q", "S", "D", "Space"]
allKeysList = ["Z", "Q", "S", "D", "Space", "W", "A"]
initWin("Anti AFK")

mainThread = None

win.startBtn.clicked.connect(main)
win.stopBtn.clicked.connect(stopMain)
win.startWithoutTimerBtn.clicked.connect(main)
win.minimizeBtn.clicked.connect(minimize)
win.exitBtn.clicked.connect(_exit)

win.azertyPreset.clicked.connect(lambda: saveMoves(["Z", "Q", "S", "D", "Space"]))
win.qwertyPreset.clicked.connect(lambda: saveMoves(["W", "A", "S", "D", "Space"]))

win.show()
App.exec()
