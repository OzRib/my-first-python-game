import tkinter as tk
import random
from pynput import keyboard

rand = lambda x:int(random.random()*x)

class Player:
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.xs1 = x*40
        self.ys1 = y*40
        self.xs2 = self.xs1+40
        self.ys2 = self.ys1+40
    
    def setX(self,x):
        self.x = x
        self.xs1 = x*40
        self.xs2 = self.xs1+40

    def setY(self,y):
        self.y = y
        self.ys1 = y*40
        self.ys2 = self.ys1+40

class Game(tk.Frame):
    player = Player()
    aceptedMoves = {
            keyboard.Key.up: lambda play:play.setY((play.y-1)),
            keyboard.Key.down: lambda play:play.setY((play.y+1)),
            keyboard.Key.left: lambda play:play.setX((play.x-1)),
            keyboard.Key.right: lambda play:play.setX((play.x+1))
    }

    commands = {
            keyboard.Key.esc: lambda self: Game.end(self)
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.lastCommand = ''
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.pack()
        Game.player.setPosition(2,3)
        self.listener.start()
        self.initCanvas()
        self.renderGame()

    def movePlayer(self, move):
        try:
            Game.aceptedMoves[move](Game.player)
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
                self.lastCommand = Game.commands[key](self)
            except:
                pass

    def initCanvas(self):
        self.canvas = tk.Canvas(self.master, bg="#32327F", height=800,width=800)
        self.canvas.pack()

    def renderGame(self):
        PLAYER = Game.player
        self.canvas.create_rectangle(0,0,800,800,fill="#32327F")
        self.canvas.create_rectangle(PLAYER.xs1,PLAYER.ys1,PLAYER.xs2,PLAYER.ys2, fill="green")

    def on_release(self, key):
        self.keyboardListener(key)

    def keyboardListener(self, key):
        self.setCommand(key)
        self.updateScreen()
        print(key)
    
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
