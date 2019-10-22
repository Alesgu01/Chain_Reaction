import copy
import math
from graphics import *
## DEFINE FUNCTIONS

### Functions for array
def genMatrix(x,y):
    result = []
    for j in range(x):
        temp = []
        for i in range(y):
            temp.append(0)
        result.append(temp)
    return result

def checkMap(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if(arr[i][j] == 0): return True
    return False

def checkmanyPl(arr):
    ch_color = 10
    pl = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if(arr[i][j] != 0 and pl == 0): pl = math.ceil(arr[i][j]/ch_color)
            elif(arr[i][j] != 0 and pl != math.ceil(arr[i][j]/ch_color)): return True
    return False

def existPl(player, arr):
    ch_color = 10
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if(math.ceil(arr[i][j]/10) == player): return True
    return False

def validMove(coord, arr, pl):
    ch_color = 10
    if (coord == [-1, -1]):
        return False
    elif (math.ceil(arr[coord[0]][coord[1]]/10) == pl+1 or arr[coord[0]][coord[1]]==0):
        return True
    else:
        return False

def blast(arr):
    ch_color = 10
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if((i == 0 or i == len(arr)-1) and (j == 0 or j == len(arr[0])-1) and arr[i][j]%ch_color >= 2):        # angolo
                #print("Blast: " + str(i) + " - " + str(j) + " - " + str(arr[i][j]))
                return True
            elif(((i == 0 or i == len(arr)-1) or (j == 0 or j == len(arr[0])-1)) and arr[i][j]%ch_color >= 3):    # lato
                #print("Blast: " + str(i) + " - " + str(j) + " - " + str(arr[i][j]))
                return True
            elif arr[i][j]%ch_color >= 4:
                #print("Blast: " + str(i) + " - " + str(j) + " - " + str(arr[i][j]))
                return True
    return False

def propagation(arr, pl, win, info):
    ch_color = 10
    printMatCIRCLE(arr, win, info)
    while(blast(arr) and checkmanyPl(arr)):
        back = copy.deepcopy(arr)
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if((i == 0 or i == len(back)-1) and (j == 0 or j == len(back[0])-1) and back[i][j]%ch_color >= 2):        # angolo
                    arr[i][j] = pl * ch_color + (back[i][j]-2)%ch_color
                    if(not(i+1 >= len(arr))):
                        arr[i+1][j] = back[i+1][j]%ch_color + ch_color*pl + 1
                    if(not(i-1 < 0)):
                        arr[i-1][j] = back[i-1][j]%ch_color + ch_color*pl + 1
                    if(not(j+1 >= len(arr[0]))):
                        arr[i][j+1] = back[i][j+1]%ch_color + ch_color*pl + 1
                    if(not(j-1 < 0)):
                        arr[i][j-1] = back[i][j-1]%ch_color + ch_color*pl + 1
                    
                elif(((i == 0 or i == len(back)-1) or (j == 0 or j == len(back[0])-1)) and back[i][j]%ch_color >= 3):    # lato
                    arr[i][j] = pl * ch_color + (back[i][j]-3)%ch_color
                    if(not(i+1 >= len(arr))):
                        arr[i+1][j] = back[i+1][j]%ch_color + ch_color*pl + 1
                    if(not(i-1 < 0)):
                        arr[i-1][j] = back[i-1][j]%ch_color + ch_color*pl + 1
                    if(not(j+1 >= len(arr[0]))):
                        arr[i][j+1] = back[i][j+1]%ch_color + ch_color*pl + 1
                    if(not(j-1 < 0)):
                        arr[i][j-1] = back[i][j-1]%ch_color + ch_color*pl + 1
                    
                elif back[i][j]%ch_color >= 4:                                                                        # interno
                    arr[i][j] = pl * ch_color + (back[i][j]-4)%ch_color
                    
                    arr[i+1][j] = back[i+1][j]%ch_color + ch_color*pl + 1
                    arr[i-1][j] = back[i-1][j]%ch_color + ch_color*pl + 1
                    arr[i][j+1] = back[i][j+1]%ch_color + ch_color*pl + 1
                    arr[i][j-1] = back[i][j-1]%ch_color + ch_color*pl + 1
        
        printMatCIRCLE(arr, win, info)    
        #win.getMouse()
    return arr

### Functions for graphics
def clear(win):
    for item in win.items[:]:
        item.undraw()

def createMat(arr, win):
    size_disp = 20
    x = ''
    ##win = GraphWin("ChainReaction", len(map)*size_disp*2, len(map[0])*size_disp*2, autoflush=False)
# creates grid
    for i in range(len(arr)-1):
        l = Line(Point((i+1)*size_disp*2, 1), Point((i+1)*size_disp*2, len(arr[0])*2*size_disp-1))
        l.draw(win)
    for j in range(len(arr[0])-1):
        l = Line(Point(1, (j+1)*size_disp*2), Point(len(arr)*2*size_disp-1, (j+1)*size_disp*2))
        l.draw(win)
# generations
    while(x != 'e'):
        inp = win.getMouse()
        #print(str(inp.getX()) + " - " + str(inp.getY()))        
        newx = math.floor(inp.getX()/(size_disp*2))
        newy = math.floor(inp.getY()/(size_disp*2))
        arr[newx][newy] += 1
        x = win.checkKey()
    ##win.close()
    return arr

def inputMat(arr, win):
    corner = 20
    newx = -1
    newy = -1
    while (newx == -1 or newy == -1):
        #x = input("HERE")
        size_disp = int((win.width-2*corner)/(2*len(arr)))
        #print("Scegli una casella: ")
        inp = win.getMouse()
        #print(str(inp.getX()) + " - " + str(inp.getY())) 
        newx = math.floor((inp.getX() - corner)/(size_disp*2))
        newy = math.floor((inp.getY() - corner)/(size_disp*2))
        if((newx < 0 or newx >= len(arr)) or (newy < 0 or newy >= len(arr[0]))):
            newx = -1
            newy = -1
    return [newx, newy]

def printMatCIRCLE(arr, win, info):
    clear(win)
    corner = 20
    size_disp = (win.width - 2*corner)/(2*len(arr))
    radius = 8
    ch_color = 10
    #win = GraphWin("ChainReaction", len(arr)*size_disp*2, len(arr[0])*size_disp*2, autoflush=False)
    try:
        
        # creates frame
        l = Line(Point(1 + corner, 1 + corner), Point(1 + corner, len(arr[0])*2*size_disp-1 + corner))
        l.draw(win)
        l = Line(Point(1 + corner, 1 + corner), Point(len(arr)*2*size_disp-1 + corner, 1 + corner))
        l.draw(win)
        l = Line(Point(len(arr)*2*size_disp-1 + corner, len(arr[0])*2*size_disp-1 + corner), Point(1 + corner, len(arr[0])*2*size_disp-1 + corner))
        l.draw(win)
        l = Line(Point(len(arr)*2*size_disp-1 + corner, len(arr[0])*2*size_disp-1 + corner), Point(len(arr)*2*size_disp-1 + corner, 1 + corner))
        l.draw(win)
        
        # creates grid
        for i in range(len(arr)-1):
            l = Line(Point((i+1)*size_disp*2 + corner, 1 + corner), Point((i+1)*size_disp*2 + corner, len(arr[0])*2*size_disp-1 + corner))
            l.draw(win)
        for j in range(len(arr[0])-1):
            l = Line(Point(1 + corner, (j+1)*size_disp*2 + corner), Point(len(arr)*2*size_disp-1 + corner, (j+1)*size_disp*2 + corner))
            l.draw(win)
        
        # puts circles
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                # drawing circles
                if(arr[i][j]%ch_color == 1):        # one circle
                    c = Circle(Point((2*i+1)*size_disp + corner, (2*j+1)*size_disp + corner), radius)
                    if math.ceil(arr[i][j]/ch_color)==1:
                        c.setFill(color_rgb(255, 0, 0))
                    elif math.ceil(arr[i][j]/ch_color)==2:
                        c.setFill(color_rgb(0, 255, 0))
                    c.draw(win)
                
                
                elif(arr[i][j]%ch_color == 2):        # two circles
                    c1 = Circle(Point((2*i+1)*size_disp + math.ceil(radius/2) + corner, (2*j+1)*size_disp + math.ceil(radius/2) + corner), radius)
                    c2 = Circle(Point((2*i+1)*size_disp - math.ceil(radius/2) + corner, (2*j+1)*size_disp - math.ceil(radius/2) + corner), radius)
                    if math.ceil(arr[i][j]/ch_color)==1:
                        c1.setFill(color_rgb(255, 0, 0))
                        c2.setFill(color_rgb(255, 0, 0))
                    elif math.ceil(arr[i][j]/ch_color)==2:
                        c1.setFill(color_rgb(0, 255, 0))
                        c2.setFill(color_rgb(0, 255, 0))
                    c1.draw(win)
                    c2.draw(win)
                    
                elif(arr[i][j]%ch_color == 3):        # three circles
                    c1 = Circle(Point((2*i+1)*size_disp + math.ceil(radius/2) + corner, (2*j+1)*size_disp + corner), radius)
                    c2 = Circle(Point((2*i+1)*size_disp - math.ceil(radius/3) + corner, (2*j+1)*size_disp + math.ceil(radius/2) + corner), radius)
                    c3 = Circle(Point((2*i+1)*size_disp - math.ceil(radius/3) + corner, (2*j+1)*size_disp - math.ceil(radius/2) + corner), radius)
                    if math.ceil(arr[i][j]/ch_color)==1:
                        c1.setFill(color_rgb(255, 0, 0))
                        c2.setFill(color_rgb(255, 0, 0))
                        c3.setFill(color_rgb(255, 0, 0))
                    elif math.ceil(arr[i][j]/ch_color)==2:
                        c1.setFill(color_rgb(0, 255, 0))
                        c2.setFill(color_rgb(0, 255, 0))
                        c3.setFill(color_rgb(0, 255, 0))
                    c1.draw(win)
                    c2.draw(win)
                    c3.draw(win)
                '''
				elif(arr[i][j]%ch_color >= 4):
                    msg = Text(Point((2*i+1)*size_disp + math.ceil(radius/2), (2*j+1)*size_disp), str(arr[i][j]%ch_color))
                    msg.draw(win)
				'''
        # puts info under graph
        center = Point(math.ceil(win.width/2), win.height - corner - 20)
        txt = Text(center, "Turn: " + str(info[0]) + "     Player: " + str(info[1]))
        txt.draw(win)
        
    except:
        print("Error Graphic")
        pass
    update(5)

## DETERMINE VARIABLES

turn = 0
players = 2
winner = 0

size_disp = 20
corner = 20
info_height = 100

map = genMatrix(16,12)
ch_color = 10

## MAIN

win = GraphWin("ChainReaction", len(map)*size_disp*2 + 2*corner, len(map[0])*size_disp*2 + 2*corner + info_height, autoflush=False)

info = [0, 0]
#x = input("HERE1")
printMatCIRCLE(map, win, info)

#x = input("HERE2")

while ((checkMap(map) and turn < players) or checkmanyPl(map)):
    turn = turn + 1
    pl = (turn-1)%players
    winner = pl + 1
    #x = input("HERE3")
    info = [turn, pl + 1]
    
    if (existPl(pl, map) or (turn <= players)):            # condition for player to play
        #x = input("HERE4")
        coord = [-1, -1]
        while(validMove(coord, map, pl) == False):        # ask for input until valid
            coord = inputMat(map, win)
        if(map[coord[0]][coord[1]] == 0):
            map[coord[0]][coord[1]] = pl*ch_color + 1
        else: 
            map[coord[0]][coord[1]] += 1
        map = propagation(map, pl, win, info)

win.close()
print("\n\n                FINISHED!   Player " + str(winner) + " won!")
x = input("\n\nPress ENTER to exit...")

'''
printMatCIRCLE(map, win)
inputMat(map, win)
printMatCIRCLE(map, win)
'''