import tkinter as tk
import random
from pynput import keyboard

rand = lambda x:int(random.random()*x)

class Thing:
    x=0
    y=0
    def __init__(self, x=x, y=y):
        self.setPosition(x=x, y=y)

    def setPosition(self, x=x, y=y):
        self.x = x
        self.y = y
        self.xs1 = x*40
        self.ys1 = y*40
        self.xs2 = self.xs1+40
        self.ys2 = self.ys1+40

class Fruit(Thing):
    def __del__(self):
        print("A fruit was deleted")

class Player(Thing):
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
    fruits = {0:Fruit(5,6)}
    ACEPTEDMOVES = {
            keyboard.Key.up: lambda play:play.setY((play.y-1)),
            keyboard.Key.down: lambda play:play.setY((play.y+1)),
            keyboard.Key.left: lambda play:play.setX((play.x-1)),
            keyboard.Key.right: lambda play:play.setX((play.x+1))
    }

    COMMANDS = {
            keyboard.Key.esc: lambda self: Game.end(self),
            keyboard.Key.f4: lambda self: Game.addFruit(self, rand(20), rand(20)),
            keyboard.Key.f10: lambda self: Game.checkPos(self)
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
    
    def addFruit(self, x,y):
        self.fruits[len(self.fruits)] = Fruit(x,y)
        print("A fruit added")

    def checkPos(self):
        print('Player position (x,y): ({px},{py})'.format(px=Game.player.x, py=Game.player.y))
        for fruitId in self.fruits:
            FRUIT = self.fruits[fruitId]
            print('Fruit position (x,y): ({fx},{fy})'.format(fx=FRUIT.x, fy=FRUIT.y)) 

    def checkColision(self):
        PLAYER = self.player
        for fruitId in self.fruits:
            FRUIT = self.fruits[fruitId]
            if FRUIT.x == PLAYER.x and FRUIT.y == PLAYER.y:
                print("Colision in ({x},{y})".format(x=FRUIT.x, y=FRUIT.y))
                self.removeFruit(fruitId)


    def removeFruit(self, id):
        del self.fruits[id]

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
            self.checkColision()
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
        for fruitId in Game.fruits:
            FRUIT = Game.fruits[fruitId]
            self.canvas.create_rectangle(FRUIT.xs1,FRUIT.ys1,FRUIT.xs2,FRUIT.ys2, fill="green")
        self.canvas.create_rectangle(PLAYER.xs1,PLAYER.ys1,PLAYER.xs2,PLAYER.ys2, fill="white")
    
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
