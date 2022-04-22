#################################################
# term project.py

# Your name: Shumiao Liu
# Your andrew id: shumiaol
#################################################

import cmu_112_graphics
import random
import math, copy, os
import pygame
from pygame import mixer
from cmu_112_graphics import *

##################sound

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)
    
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())
    
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    def stop(self):
        pygame.mixer.music.stop()

########### create player and protecter

class player:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.protect = []
        #self.matrixx = self.cx/(540/40)
        #self.matrixy

cx = 300
cy = 250
players = player(cx, cy)

########### create protector

class protector:
    def __init__(self,px,py):
        self.px = px
        self.py = py

########### create attacker

class attacker:
    def __init__(self):
        c = random.choice([1,2,3,4])
        if c == 1:
            attackerX = 0
            attackerY = random.randint(0, 540)
        elif c == 2:
            attackerX = 960
            attackerY = random.randint(0, 540)
        elif c == 3:
            attackerX = random.randint(0, 960)
            attackerY = 0
        elif c == 4:
            attackerX = random.randint(0, 960)
            attackerY = 540
        self.X = attackerX
        self.Y = attackerY
        self.speed = random.randint(8,9)

########### create weapon

class weapon:
    def __init__(self):
        self.dirx = 0
        self.diry = 0
        self.startx = 0
        self.starty = 0

########### create increase

class increase:
    def __init__(self):
        addX = random.randint(0,960)
        addY = random.randint(0,540)
        self.inX = addX
        self.inY = addY

############### create pathfinder

class Pathfinder:
    def __init__(self, last = None, position = None):
        self.matrix = matrix
        self.locationX = 0
        self.locationY = 0
        self.location = 0
        self.last = last
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self,other):
        return self.position == other.position

matrix = [
	[2,2,2,2,2,2,2,2,2,2,2,3,2,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,3],#0
	[2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,3],#1
	[2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#2
	[1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],#3
	[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],#4
	[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,5,2,2,2,2,5,5,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],#5
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],#6
	[0,0,0,0,0,0,0,0,0,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,3],#7
	[1,1,1,1,1,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,3],#8
	[1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5],#9
	[1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5],#10
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#11
	[0,0,0,0,5,5,5,5,5,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#12
	[0,0,0,0,5,2,2,2,2,5,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,5,5,5,5,5,5,5],#13
	[0,0,0,0,5,5,5,5,5,5,5,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,5,2,2,2,2,2,2,2],#14
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,5,5,5],#15
	[0,1,1,1,0,0,1,0,0,0,5,5,5,5,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#16
	[1,1,1,1,1,1,1,1,0,0,5,5,5,5,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,3],#17
	[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,3],#18
	[0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0],#19
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#20
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,2,2,2,2,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#21
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,2,2,2,2,2,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]#22
    #0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9

possibleW = []
possibleP = []
rows = len(matrix)
cols = len(matrix[0])
for row in range(rows):
    for col in range(cols):
        index = matrix[row][col]
        if index == 5:
            possibleW.append((row,col))
        elif index == 0:
            possibleP.append((row,col))

pathfinder = Pathfinder()

############# create stage2 weapon

class newAttacker:
    def __init__(self,start):
        self.start = start
        self.X = start[0]
        self.Y = start[1]

################ main

def appStarted(app):
    app.stage1 = True
    app.stage2 = False
    app.stage3 = False
    if app.stage2 == True:
        app.cx = app.width-20
        app.cy = app.height-20
    elif app.stage1 == True:
        app.cx = app.width/2
        app.cy = app.height/2
    app.r = 15

    app.add = 0
    app.stage2Add = []
    app.protector = []
    app.procount = 0 
    app.prox = [-30,0,30,30,30,0,-30,-30]
    app.proy = [30,30,30,0,-30,-30,-30,0]

    app.len = 30
    #protecter location
    app.increase = [(app.width/3,app.height/3),((2*app.width)/3,
                    (2*app.height)/3), (app.width/3,(2*app.height)/3),
                    ((2*app.width)/3,app.height/3)]
    #app.increase2 = 
    app.attack = []
    app.newAttack = []
    app.attcount = 0
    app.attcount2 = 0
    app.attcount3 = 0
    app.matrixRatio = app.width/len(matrix[0])

    app.move = 0
    app.stage2c = 0

    app.timePassed = 0
    app.score = 0
    app.startmenu = True
    app.worL = None
    app.stage1Pass = None
    app.stageload = 0

    app.weaponLeft = 15
    app.weapon = []

    #sound
    pygame.mixer.init()
    #app.soundW = Sound("button.mp3") 
    app.soundA = Sound("add.wav") 
    app.soundE = Sound("explosion.ogg") 
    #app.soundback = Sound("background.ogg")

    #art asset
    app.image1 = app.loadImage('stage1background.jpg')
    app.image11 = app.scaleImage(app.image1, 1/2)
    app.image2 = app.loadImage('start.jpg')
    app.image22 = app.scaleImage(app.image2, 1/2)
    app.image3 = app.loadImage('stage2background.jpg')
    app.image33 = app.scaleImage(app.image3, 1/2)
    app.image4 = app.loadImage('lose.jpg')
    app.image44 = app.scaleImage(app.image4, 1/2)
    app.image5 = app.loadImage('stage1 pass.jpg')
    app.image55 = app.scaleImage(app.image5, 1/2)
    app.image6 = app.loadImage('cloud.png')
    app.image66 = app.scaleImage(app.image6, 1/2)
    app.image7 = app.loadImage('stage2 pass.jpg')
    app.image77 = app.scaleImage(app.image7, 1/2)
    app.imagep = app.loadImage('player.png')
    app.imagepp = app.scaleImage(app.imagep, 1/5)
    app.imagea = app.loadImage('attacker.png')
    app.imageaa = app.scaleImage(app.imagea, 1/10)
    app.imagepro = app.loadImage('protect.png')
    app.imageppro = app.scaleImage(app.imagepro, 1/10)
    app.imageadd = app.loadImage('add.png')
    app.imageaadd = app.scaleImage(app.imageadd, 1/5)

#def appStopped(app):
    #app.soundW.stop()

def mousePressed(app, event):
    app.wx = event.x
    app.wy = event.y
    addWeapon(app)
    app.startmenu = False
    #if app.worL == False:
    if app.stageload == 0:
        if app.worL == False:
            app.stage1 = True
            resetstage1(app)
            app.worL = None
    if app.stageload == 1:
        print(app.worL)
        if app.worL == False:
            app.stage2 = True
            resetstage2(app)
            app.worL = None
        elif app.worL:
            app.stage2 = True
            resetstage2(app)
            app.stageload = 1
            app.worL = None
    if app.stageload == 2:
        if app.worL:
            app.stage3 = True
            resetstage3(app)
            app.worL = None

def keyPressed(app, event):
    if (event.key in ['a','A']):
        app.move += 1
        mx = -5
        my = 0
        if whetherMove(app,mx,my):
            if len(app.protector) > 0:
                for protector in app.protector:
                    if (app.cx > 40):
                        protector.px -= 5
                        app.cx -= 5/len(app.protector)
            else:
                if (app.cx - app.r >=5 ):
                    app.cx -= 5
    elif (event.key in ['d','D']):
        app.move += 1
        mx = 5
        my = 0
        if whetherMove(app,mx,my):
            if len(app.protector) > 0:
                for protector in app.protector:
                    if (app.cx < app.width - 40):
                        protector.px += 5
                        app.cx += 5/len(app.protector)
            else:
                if (app.cx + app.r <= app.width-5):
                    app.cx += 5
    elif (event.key in ['w','W']):
        app.move += 1
        mx = 0
        my = -5
        if whetherMove(app,mx,my):
            if len(app.protector) > 0:
                for protector in app.protector:
                    if (app.cy > 40):
                        protector.py -= 5
                        app.cy -= 5/len(app.protector)
            else:
                if (app.cy - app.r >= 5):
                    app.cy -= 5
    elif (event.key in ['s','S']):
        app.move += 1
        mx = 0
        my = 5
        if whetherMove(app,mx,my):
            if len(app.protector) > 0:
                for protector in app.protector:
                    if (app.cy < app.height - 40):
                        protector.py += 5
                        app.cy += 5/len(app.protector)
            else:
                if (app.cy + app.r <= app.height - 5):
                    app.cy += 5
    if app.stage1:
        eat(app)
    if app.stage2:
        eat2(app)
        whetherAdd(app)

def whetherAdd(app):
        if app.move == 20:
                if addAttacker(app):
                    fighter2 = newAttacker(random.choice(possibleW))
                    #print('p',possibleW)
                    app.newAttack.append(fighter2)
                    app.attcount3 = app.attcount
                    app.move = 0    

def whetherMove(app, mx, my):
    pathfinder.locationY = math.floor((app.cx+mx)/(app.matrixRatio))
    pathfinder.locationX = math.floor((app.cy+my)/(app.matrixRatio))
    pathfinder.location = matrix[pathfinder.locationX]\
                                    [pathfinder.locationY]
    if app.stage2 == True:
	    if pathfinder.location == 1 or pathfinder.location == 2 or \
                pathfinder.location == 5:
		    return False
	    elif pathfinder.location == 0 or \
                    pathfinder.location == 3 or pathfinder.location == 4:
		    return True
    else: return True
    
def transfer(app,x):
    row = x[0]
    col = x[1]
    cx = col * app.matrixRatio + app.matrixRatio/2
    cy = row * app.matrixRatio + app.matrixRatio/2
    return (cx,cy)

#pathfinding helper function
def inList (child,closed_list):
    for closed_child in closed_list:
        if child == closed_child:
            return True

def aStar(app, matrix, start_position):
    end = (math.floor((app.cy)/(app.height/23)),
                math.floor((app.cx)/(app.width/40)))
    start = start_position#random.choice(possibleW)

    startNode = Pathfinder(None, start)
    endNode = Pathfinder(None, end)

    openList = []
    closeList = []
    openList.append(startNode)
    while len(openList)>0:
        pos = openList[0]
        index = 0
        for i in range(len(openList)):
            if openList[i].f < pos.f:
                index = i
                pos = openList[i]

        if pos == endNode:
            movePath = []
            step = pos
            while step is not None:
                movePath.append(step.position)
                step = step.last
            return movePath[::-1]

        openList.pop(index)
        closeList.append(pos)
        nextMove = []
        nx = [0,0,-1,1]
        ny = [-1,1,0,0]
        count = 4
        for i in range(count):
            newPosition = (pos.position[0]+nx[i], 
                            pos.position[1]+ny[i])
            if newPosition[0] > len(matrix)-1 or newPosition[0]<0 or \
                    newPosition[1]> len(matrix[0])-1 or newPosition[1] < 0:
                continue
            elif matrix[newPosition[0]][newPosition[1]] not in [0,3,4]:
                continue
            newNode = Pathfinder(pos, newPosition)
            nextMove.append(newNode)
        
        for move in nextMove:
            if inList(move,closeList):
                continue
            move.g = pos.g + 1 #steps already
            move.h = abs(move.position[0]-endNode.position[0]) + \
                    abs(move.position[1]-endNode.position[1]) #distance/how far
            move.f = move.g + move.h #total cost

            if not inList(move, openList):
                openList.append(move)
            else:
                for open_node in openList:
                    if move == open_node and move.g < open_node.g:
                        open_node = move
          
def timerFired(app):
    #addAttacker(app)
    if app.stage1 == True:
        if app.timePassed % 700 == 0:
            if addAttacker(app):
                fighter = attacker()
                app.attack.append(fighter)
                app.attcount2 = app.attcount
        moveAttacker(app)
        moveWeapon(app)
    elif app.stage2 == True:
        if app.timePassed % 400 == 0:
            movenewAttacker(app)
        if app.timePassed % 2000 == 0:
            addShow(app)
        moveWeapon(app)
    app.timePassed += app.timerDelay

def moveAttacker(app):
    for attacker in app.attack:
            dist = math.sqrt((app.cx - attacker.X)**2 + 
                        (app.cy - attacker.Y)**2)
            attacker.X += attacker.speed * (app.cx - attacker.X)/dist
            attacker.Y += attacker.speed * (app.cy - attacker.Y)/dist
            if not hurtProtect(app,attacker):
                hurtPlayer(app,attacker)
    if app.attcount2 == 20 and app.add == 4:
        if len(app.attack) == 0:
            app.stage1 = False
            app.stage2 = True
            app.worL = True
            app.stageload = 1
            resetstage2(app)

def movenewAttacker(app):
    for attacker2 in app.newAttack:
        movement = aStar(app, matrix, attacker2.start)
        if movement is None : continue
        elif len(movement) == 1: 
            continue
        else:
            cord = transfer(app,movement[1])
            attacker2.X = cord[0]
            attacker2.Y = cord[1]
            attacker2.start = movement[1]
        if not hurtProtect(app,attacker2):
            hurtPlayer(app,attacker2)
        #print('movement',movement)
        #print('m4',movement[1][0])
        #print('m40',movement[1][1])
    if app.score == 10 and app.add == 4:
        if len(app.newAttack) == 0:
            app.stage2 = False
            app.stage3 = True
            app.worL = True
            app.stageload = 2
            resetstage3(app)

def addAttacker(app):
    if app.stage1 == True:
        if app.add >= 2:
            app.attcount += 1
            if app.attcount <= 20:
                return True
    elif app.stage2 == True:
        app.attcount += 1
        if app.attcount <= 15:
            return True

def resetstage1(app):
    app.cx = app.width//2
    app.cy = app.height//2
    app.attcount = 0
    app.attcount2 = 0
    app.attack = []
    app.protector = []
    app.procount = 0
    app.add = 0
    app.weapon = []
    app.score = 0
    app.increase = [(app.width/3,app.height/3),((2*app.width)/3,
                    (2*app.height)/3), (app.width/3,(2*app.height)/3),
                    ((2*app.width)/3,app.height/3)]

def resetstage2(app):
    app.cx = app.width - 20
    app.cy = app.height - 20
    app.attcount = 0
    app.attcount2 += 1
    app.newAttack = []
    app.protector = []
    app.procount = 0
    app.add = 0
    app.weapon = []
    app.score = 0
    app.move = 0
    app.stage2Add = []

def hurtProtect(app,attacker):
    ind = False
    for protect in app.protector:
        dist = math.sqrt(abs(protect.px - attacker.X)**2 + \
                abs(protect.py - attacker.Y)**2)
        if dist <= 16:
            app.protector.remove(protect)
            if app.stage1:
                app.attack.remove(attacker)
            elif app.stage2:
                app.newAttack.remove(attacker)
            app.score += 1
            ind = True
    return ind

def hurtPlayer(app,attacker):
    dist = math.sqrt(abs(app.cx - attacker.X)**2 + \
                abs(app.cy - attacker.Y)**2)
    if dist <= app.r + 10:
        #app.attack.remove(attacker)
        app.worL = False

def hurtEne(app,weapon):
    ind = False
    if app.stage1:
        for attacker in app.attack:
            dist = math.sqrt(abs(weapon.startx - attacker.X)**2 + \
                    abs(weapon.starty - attacker.Y)**2)
            if dist <= 15:
                app.soundE.start()
                app.attack.remove(attacker)
                app.score += 1
                ind = True
        return ind
    elif app.stage2:
        for attacker in app.newAttack:
            dist = math.sqrt(abs(weapon.startx - attacker.X)**2 + \
                    abs(weapon.starty - attacker.Y)**2)
            if dist <= 15:
                app.newAttack.remove(attacker)
                app.score += 1
                ind = True
        return ind
            
def moveWeapon(app):
    for weapon in app.weapon:
            dist = math.sqrt(weapon.dirx**2 + weapon.diry**2)
            weapon.startx += 13 * weapon.dirx/dist
            weapon.starty += 13 * weapon.diry/dist
            if hurtEne(app,weapon):
                app.weapon.remove(weapon)

def addWeapon(app):
    weapon1 = weapon()
    weapon1.startx = app.cx
    weapon1.starty = app.cy
    weapon1.dirx = app.wx - app.cx
    weapon1.diry = app.wy - app.cy
    if len(app.weapon) < 15:
        app.weapon.append(weapon1)

###if plyer eat all the "add", attacker will show up
def eat(app):
    r = 15
    for (x,y) in app.increase:
        if math.sqrt((app.cx - x)**2 + (app.cy - y)**2) < (app.r + r):
            app.increase.remove((x,y))
            app.soundA.start()
            app.add += 1
            p = app.procount
            pro1 = protector(app.cx + app.prox[p],app.cy + app.proy[p])
            pro2 = protector(app.cx + app.prox[p+1],app.cy + app.proy[p+1])
            app.procount += 2
            app.protector.append(pro1)
            app.protector.append(pro2)

def addShow(app):
    if app.stage2c < 4:
        #app.add += 1
        pro = transfer(app,random.choice(possibleP))
        app.stage2Add.append(pro)
        app.stage2c += 1 

def eat2(app):
    r = 15
    for (x,y) in app.stage2Add:
        if math.sqrt((app.cx - x)**2 + (app.cy - y)**2) < (app.r + r):
            app.stage2Add.remove((x,y))
            app.soundA.start()
            p = app.procount
            pro1 = protector(app.cx + app.prox[p],app.cy + app.proy[p])
            pro2 = protector(app.cx + app.prox[p+1],app.cy + app.proy[p+1])
            app.procount += 2
            app.protector.append(pro1)
            app.protector.append(pro2)
            app.add+=1

################ Draw ###############

def drawWeapon(app, canvas):
    r = 5
    for weapon in app.weapon:
        color = random.choice(['red','yellow','blue'])
        canvas.create_oval(weapon.startx-r, weapon.starty-r,
                        weapon.startx+r, weapon.starty+r,
                        fill = color,
                        width = 0)

def drawProtect(app,canvas):
    r = 6
    for protect in app.protector:
        canvas.create_image(protect.px, protect.py, 
                image=ImageTk.PhotoImage(app.imageppro))

def drawAttacker(app,canvas):
    r = 10
    for attack in app.attack:
        canvas.create_image(attack.X, attack.Y, 
                image=ImageTk.PhotoImage(app.imageaa))

def drawnewAttacker(app,canvas):
    r = 10
    for attacker2 in app.newAttack:
        #color = random.choice(['red','blue','green'])
        canvas.create_image(attacker2.X, attacker2.Y, 
                image=ImageTk.PhotoImage(app.imageaa))

def drawAdd(app,canvas):
    for (x,y) in app.increase:
        addx = x
        addy = y
        canvas.create_image(addx, addy, 
                image=ImageTk.PhotoImage(app.imageaadd))

def drawnewAdd(app,canvas):
    for (x,y) in app.stage2Add:
        addx = x
        addy = y
        canvas.create_image(addx, addy, 
                image=ImageTk.PhotoImage(app.imageaadd))

def drawStartmenu(app, canvas):
    if app.startmenu == True:
        canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image22))

def drawLose(app,canvas):
    canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image44))

def drawPass(app,canvas):
    if app.stage2:
        canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image55))
    elif app.stage3:
        canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image77))

def drawStage1(app,canvas):
    canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image11))
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.imagepp))
    canvas.create_text(app.width/9, 40,
                       text= f'{app.add} / 4',
                       fill='white',
                       font = 'Arial 20 bold')
    canvas.create_text(app.width/3.5, 40,
                       text= f'{app.score} / 20',
                       fill='white',
                       font = 'Arial 20 bold')
    drawWeapon(app, canvas)
    drawAttacker(app,canvas)
    drawAdd(app,canvas)
    drawProtect(app,canvas)

def drawStage2(app,canvas):
    canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image33))
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.imagepp))
    drawProtect(app,canvas)
    canvas.create_image(480, 270, image=ImageTk.PhotoImage(app.image66))
    canvas.create_text(app.width/9, 40,
                       text= f'{app.add} / 4',
                       fill='white',
                       font = 'Arial 20 bold')
    canvas.create_text(app.width/3.5, 40,
                       text= f'{app.score} / 10',
                       fill='white',
                       font = 'Arial 20 bold')
    drawWeapon(app, canvas)
    drawnewAttacker(app,canvas)
    drawnewAdd(app,canvas)
    
def redrawAll(app, canvas):
    if app.stage1 == True:
        drawStage1(app,canvas)
    elif app.stage2 == True:
        drawStage2(app,canvas)
    if app.worL == False:
        drawLose(app,canvas)
    if app.worL:
        drawPass(app,canvas)
    drawStartmenu(app, canvas)

runApp(width=960, height=552)
