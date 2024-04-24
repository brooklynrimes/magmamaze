# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:36:12 2024

@author: Brooklyn
"""

import pygame, simpleGE, random


def myData():
    inFile = open("myData.txt", "r")
    myData = []
    for line in inFile:
        line = (line.strip("][\n").split(", "))
        temp = []
        for string in line:
            temp.append(int(string))
        myData.append(temp)
    inFile.close()
    return myData

def getPlayData():
    inFile = open("myData.txt", "r")
    myData = []
    for line in inFile:
        line = (line.strip("][\n").split(", "))
        temp = []
        for string in line:
            temp.append(int(string))
        myData.append(temp)
    inFile.close()
    return myData

class Tile(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = [
            pygame.image.load("lava1.png"),
            pygame.image.load("stone1.png"),
            pygame.image.load("dirt1.png")]
        
        self.stateName = ["lava", "stone" , "dirt"]
        
        self.setSize(48,48)
        self.LAVA = 0
        self.STONE = 1
        self.DIRT= 2 
        self.state = self.LAVA
        #self.clicked = False
        
    def setState(self, state):
    
        self.state = state
        self.copyImage(self.images[state])
        self.setSize(48,48)
        
    def process(self):
        if self.clicked:
            newState = self.state + 1
            if newState > 2:
                newState = 0
            self.setState(newState)
            
        if self.state == 0:
            if self.collidesWith(self.scene.player):
                self.scene.player.moveSpeed = .5
        if self.state == 1:
            if self.collidesWith(self.scene.player):
                self.scene.player.moveSpeed = 2
        if self.state == 2:
            if self.collidesWith(self.scene.player):
                self.scene.player.moveSpeed = 4
            
class Magma(simpleGE.Sprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.setImage("lavaball1.png")
        self.setSize(20,20)
        self.setBoundAction(self.HIDE)
        self.hide()
        
    def fire(self):
        self.show()
        self.position = self.parent.position
        self.moveAngle =( self.parent.animRow +1) * 90
        
        self.speed = 10
     
            
            
class Player(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setBoundAction("STOP") 
        self.position = (320, 235)
        self.hitPoints = 15
        self.moveAnim = simpleGE.SpriteSheet("anim1.png", (64,64), 4, 9, .1)
                                             
        self.moveAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 2
        self.jump = False
        self.move = False 
        self.bottom = True
        self.tileState = 0
      # self.tileset =self.tile
    def process(self):
        self.dx = 0
        self.dy = 0
       #tile = self.tileset
       # if self.jump:
       #     self.addForce(.2, 270)
       # if self.y > 450:
     #      # self.jump = False 
          #  self.y = 450
          #  self.dy = 0
      # self.x += self.dx
      # self.y += self.dy
      # self.vel_y = -15
       #self.dy += self.vel_y
       #move = False 
       #self.inAir = True 
      # self.jump = False 
        
        if self.isKeyPressed(pygame.K_UP):
            self.animRow = 0
            self.dy = -self.moveSpeed
            self.move = True
        if self.isKeyPressed(pygame.K_DOWN):
            self.animrow = 2
            self.dy = self.moveSpeed 
            self.move= True 
        if self.isKeyPressed(pygame.K_LEFT):
            self.animRow = 1
            self.dx = -self.moveSpeed
            self.move = True 
        if self.isKeyPressed(pygame.K_RIGHT):
            self.animRow = 3
            self.dx = self.moveSpeed
            self.move = True 
        if self.isKeyPressed(pygame.K_SPACE):
            for magma in self.scene.magma :
                magma.fire()
                
            
        if self.move:
            self.copyImage(self.moveAnim.getNext(self.animRow))
        else:
            self.copyImage(self.moveAnim.getCellImage(0, self.animRow))
        
class Enemy(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("monster1.png")
        self.setSize(40,40)
       #self.moveAnim = simpleGE.SpriteSheet("anim2.png", (64,64), 4, 9, .1)
        self.reset()
        
    def reset(self):
        edge = random.randint(0,1)
        if edge == 1:
            self.y = 10
            self.x = random.randint(5,10)
            self.moveAngle = random.randint(180, 360)
            self.speed = 1
            
class lblHealth(simpleGE.Label):
    def __init__ (self):
        super().__init__()
        self.bgColor = "red"
        self.fgColor = "black"
        self.text = "Health: 12" 
        self.position = (320, 30)
        
class lblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.bgColor = "red"
        self.fgColor = "black"
        self.text = "Time Left: 30"
        self.timer = simpleGE.Timer()
        self.center = (540, 30)
        
class lblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text= "Score 0"
        self.center = (100,30)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Magma Maze")
        self.tileset=[] 
        self.player = Player(self)
        self.timer = simpleGE.Timer()
        self.score = 0
        self.lblScore = lblScore()
        self.lblHealth = lblHealth()
        self.lblTime = lblTime()
        
       #self.magma = Magma(self, self.player)
        self.numEnemy = 11
        
        
        self.enemy =[]
        for i in range(self.numEnemy):
            self.enemy.append(Enemy(self))
            
        self.numMagma = 50
        self.currentMagma = 0
        
        self.magma = []
        for i in range(self.numMagma):
            self.magma.append(Magma(self, self.player))
        
        
        self.ROWS = 10
        self.COLS = 15
        #self.loadData()
        
        #self.data = 0
        
        #self.data()
        self.getData()
        
       # self.wall = simpleGE.Sprite(self)
        
        self.sprites = [self.tileset, self.player, self.enemy, self.magma, self.lblHealth, self.lblScore, self.lblTime]
        #self.getData()
        
    def process(self):
        for enemy in self.enemy:
            if self.player.collidesWith(enemy):
                enemy.reset()
                self.player.hitPoints -= 1 
                self.lblHealth.text = f" Health: {self.player.hitPoints}"
                
    
            
        for magma in self.magma:
            for enemy in self.enemy:
                if magma.collidesWith(enemy):
                    self.score += 1 
                    self.lblScore.text = f"Score: {self.score}"
                    enemy.reset()
                    
        self.lblTime.text = f" Time Left: {self.timer.getTimeLeft():.2f}"
        
        if self.player.hitPoints <= 0:
            self.STOP()
            
        def processEvent(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.currentMagma += 1
                    if self.currentMagma >= self.numMagma:
                        self.currentMagma = 0 
                        self.magma[self.currentMagma].fire ()
                    
                
                
                                        
        
    def loadData(self):
            data = [
            [2,1,1,1,1,1,0,0,0,1,1,1,1,1,2],
            [2,1,1,1,1,1,0,0,0,1,1,1,1,1,2],
            [2,1,1,1,1,1,0,0,0,1,1,1,1,1,2],
            [2,1,1,1,1,1,0,0,0,1,1,1,1,1,2],
            [2,1,1,1,1,1,0,0,0,1,1,1,1,1,2],
            [2,1,1,1,0,0,0,0,0,0,0,1,1,1,2],
            [2,1,1,1,0,0,0,0,0,0,0,1,1,1,2],
            [2,1,1,1,0,0,0,0,0,0,0,1,1,1,2],
            [2,1,1,1,0,0,0,0,0,0,0,1,1,1,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ]
            return data
        
    def data(self):
        run = True 
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    
            pygame.display.update()
    
    def draw(self):
        for tile in self.tile_list:
           # data.blit(tile[0], tile[1])
           pass 
    def getData(self):

        self.data = self.loadData()
        
        for row in range(self.ROWS):
            self.tileset.append([])
            for col in range(self.COLS):
                currentVal = self.data[row][col]
                newTile = Tile(self)
                newTile.setState(currentVal)
                xPos = 20 + (42.6 * col)
                yPos = 24 + (48 * row)
                newTile.x = xPos
                newTile.y = yPos
                self.tileset[row].append(newTile)
                
class Instructions(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        self.setImage("lavabckgrnd1.png")
        self.status= "Quit"
        self.score = score 
        
        self.Instructions= simpleGE.MultiLabel() 
        self.Instructions.textLines = [
            " In the maze of fiery glow", 
            " Where magma and lava flows", 
            " We feel the heat on this day", 
            " Get through the lava, and save the day",
            " Press arrow keys to move",
            " Press space bar to shoot"
            ]
        
        self.Instructions.center = (320,240)
        self.Instructions.size = (400,250)
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320,50)
        self.lblScore.size = (400,30)
        self.lblScore.text = f" Previous Score: {self.score} "
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (100,450)
        self.btnPlay.text = "Play (up)"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (540, 450)
        self.btnQuit.text = "Quit (down)"
        self.sprites = [self.lblScore, self.Instructions, self.btnPlay, self.btnQuit]
        
    def process(self):
        if self.btnPlay.clicked:
            self.status= "play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.status ="quit"
            self.stop()
            
        if self.isKeyPressed(pygame.K_UP):
            self.status ="play"
            self.stop()
            
        if self.isKeyPressed(pygame.K_DOWN):
            self.status = "quit"
            self.stop()
               
                
def main():
    pygame.display.set_caption("Magma Maze")
    
    keepGoing = True 
    score = 0 
    while keepGoing:
        instructions = Instructions(score)
        instructions.start()
        print(instructions.status)
        
        if instructions.status == "play":
            game = Game()
            game.start()
            score = game.score
            
        else:
            keepGoing = False 
  
        
if __name__ == "__main__":
    main()
        
        