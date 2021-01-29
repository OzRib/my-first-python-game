import tkinter as tk
import random
from pynput import keyboard

rand = lambda x:int(random.random()*x)

class Player:
    x=0
    y=0 
    def setPosition(self, x=x, y=y):
        self.x = x
        self.y = y
        self.xs1 = x*40
        self.ys1 = y*40
        self.xs2 = self.xs1+40
        self.ys2 = self.ys1+40

    def __init__(self, x=x, y=y):
        self.setPosition(x=x,y=y)

    def setX(self, x):
        self.setPosition(x=x, y=self.y)

    def setY(self, y):
        self.setPosition(y=y, x=self.x)

class keyboardListener:
    def init(self):
        self.listener = keyboard.Listener(on_release=self.on_release)

    def on_release(self, key):
        self.Listener(key)

    def setListener(self, on_event, callback):
        self.on_event = on_event
        self.callback = callback

    def Listener(self, key):
        self.on_event(key)
        self.callback()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

class Game(tk.Frame):
    player = Player(2,3)
    ACEPTEDMOVES = {
            keyboard.Key.up: lambda play:play.setY((play.y-1)),
            keyboard.Key.down: lambda play:play.setY((play.y+1)),
            keyboard.Key.left: lambda play:play.setX((play.x-1)),
            keyboard.Key.right: lambda play:play.setX((play.x+1))
    }

    COMMANDS = {
            keyboard.Key.esc: lambda self: Game.end(self)
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.lastCommand = ''
        self.listener = keyboardListener()
        self.listener.setListener(self.setCommand, self.updateScreen)
        self.listener.init()
        self.pack()
        self.listener.start()
        self.initCanvas()
        self.renderGame()

    def movePlayer(self, move):
        PLAYER = self.player
        RULES = {
                keyboard.Key.up: PLAYER.y>0,
                keyboard.Key.down: PLAYER.y<19,
                keyboard.Key.left: PLAYER.x>0,
                keyboard.Key.right: PLAYER.x<19
        }
        try:
            if RULES[move]:
                self.ACEPTEDMOVES[move](self.player)
                print("moved player with {m}".format(m=move))
            print("Player x: {px} Player y: {py}".format(px=Game.player.x, py=Game.player.y))
            return True
        except:
            return False

    def setCommand(self, key):
        if self.movePlayer(key):
            pass
        else:
            try:
                self.lastCommand = self.COMMANDS[key](self)
            except:
                pass

    def initCanvas(self):
        self.canvas = tk.Canvas(self.master, bg="#32327F", height=800,width=800)
        self.canvas.pack()

    def renderGame(self):
        PLAYER = Game.player
        self.canvas.create_rectangle(0,0,800,800,fill="#32327F")
        self.canvas.create_rectangle(PLAYER.xs1,PLAYER.ys1,PLAYER.xs2,PLAYER.ys2, fill="green")
    
    def updateScreen(self):
        if self.lastCommand == 'end':
            pass
        else:
            self.renderGame()
            self.update()

    def end(self):
        self.listener.stop()
        self.quit()
        print('gameover')
        return 'end'

root = tk.Tk()
root.title('Game')
root.geometry("800x800")

game = Game(master=root)
game.mainloop()

try:
    game.listener.stop()
except:
    pass
