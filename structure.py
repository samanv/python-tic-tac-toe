import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random

grid = [['','',''],['','',''],['','','']]
cell = [[],[],[]]

color = dict()

lastX = 0
lastY = 0

firstX = 0
firstY = 0

PLAYER = "X"
COMPUTER = "O"

color[PLAYER] = '#3983B1'
color[COMPUTER] = '#EA202A'

sides = [[0,1],[1,0],[1,2],[2,1]]
corners = [[0,0],[0,2],[2,2],[2,0]]

totalMoves = 0

def gridFull():
    if ('' not in grid[0]) and ('' not in grid[1]) and ('' not in grid[2]):
        return True
    else:
        return False

def getOpen():

    for i in range(3):
        for j in range(3):
            if not grid[i][j]:
                return [i,j]

def isThreat():

    if grid[lastX].count(PLAYER)==2 and grid[lastX].count('')==1:
        return 'R'

    col = [grid[0][lastY],grid[1][lastY],grid[2][lastY]]
    if col.count(PLAYER)==2 and col.count('')==1:
        return 'C'

    diag1 = [grid[0][0],grid[1][1],grid[2][2]]
    if diag1.count(PLAYER)==2 and diag1.count('')==1:
        return 'D1'

    diag2 = [grid[0][2],grid[1][1],grid[2][0]]
    if diag2.count(PLAYER)==2 and diag2.count('')==1:
        return 'D2'

    return False

def removeThreat(pos):

    global grid

    if pos == 'R':
        for i in range(3):
            if not grid[lastX][i]:
                grid[lastX][i] = COMPUTER
                return [lastX,i]

    elif pos == 'C':
        for i in range(3):
            if not grid[i][lastY]:
                grid[i][lastY] = COMPUTER
                return [i,lastY]

    elif pos == 'D1':
        for i in range(3):
            if not grid[i][i]:
                grid[i][i] = COMPUTER
                return [i,i]

    elif pos == 'D2':
        for i in range(3):
            if not grid[i][2-i]:
                grid[i][2-i] = COMPUTER
                return [i,2-i]

def checkWin():

    for i in range(3):
        if grid[i].count(COMPUTER)==2 and grid[i].count('')==1:
            return [i,grid[i].index('')]

    for i in range(3):
        col = [grid[0][i],grid[1][i],grid[2][i]]
        if col.count(COMPUTER)==2 and col.count('')==1:
            return [col.index(''),i]

    diag1 = [grid[0][0],grid[1][1],grid[2][2]]
    if diag1.count(COMPUTER)==2 and diag1.count('')==1:
        return [diag1.index(''),diag1.index('')]

    diag2 = [grid[0][2],grid[1][1],grid[2][0]]
    if diag2.count(COMPUTER)==2 and diag2.count('')==1:
        return [diag2.index(''),abs(diag2.index('')-2)]

    return False

def makeMove(i,j,value):
    grid[i][j] = value
    cell[i][j].changeTo(value)

class Cell(QLabel):

    def __init__(self,win,a,b,offset_x,offset_y,dim_x,dim_y):
        self.i = a
        self.j = b
        self.set = False
        self.label = self.makeLabel(win,offset_x, offset_y,dim_x,dim_y)
        self.label.mouseReleaseEvent = self.clicked

    def makeLabel(self,win,offset_x, offset_y,dim_x,dim_y):
        label = QLabel(win)
        label.setGeometry(offset_x, offset_y,dim_x,dim_y)
        label.setStyleSheet("background-color:#CCC;")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setCursor(QCursor(Qt.PointingHandCursor))
        return label

    def changeTo(self, value):
        global grid,totalMoves
        if not self.set:
            totalMoves += 1
            self.label.setStyleSheet("color:#FFF; font-size:18pt; font-weight:700; background-color:"+color[value])
            self.label.setText(value)
            self.label.setCursor(QCursor(Qt.ForbiddenCursor))
            grid[self.i][self.j] = value
            self.set = True
        else:
            pass

    def reset(self):
        self.label.setStyleSheet("background-color:#CCC;")
        self.label.setText("")
        self.label.setCursor(QCursor(Qt.PointingHandCursor))
        self.set = False

    def clicked(self,event):
        if self.set:
            return
        self.changeTo(PLAYER)
        global lastX, lastY, cell
        lastX = self.i
        lastY = self.j
        threat = isThreat()
        if checkWin():
            winPos = checkWin()
            makeMove(winPos[0],winPos[1],COMPUTER)
            print "COMPUTER Wins"
        elif threat:
            newPos = removeThreat(threat)
            cell[newPos[0]][newPos[1]].changeTo(COMPUTER)
        elif not grid[1][1] and [lastX,lastY] in sides:
            makeMove(1,1,COMPUTER)
        elif [lastX,lastY] == [1,1]:
            makeMove(abs(firstX-2),abs(firstY-2),COMPUTER)
        elif [lastX,lastY] in corners and  not grid[abs(lastX-2)][abs(lastY-2)]:
            if COMPUTER in grid[lastX]:
                makeMove(abs(firstX-1),abs(firstY-2),COMPUTER)
            else:
                makeMove(abs(firstX-2),abs(firstY-1),COMPUTER)
        elif [lastX,lastY] == [abs(firstX-2),abs(firstY-2)]:
            makeMove(1,1,COMPUTER)
        elif not grid[abs(lastX-1)][abs(lastY-2)]:
            makeMove(abs(firstX-1),abs(firstY-2),COMPUTER)
        elif not grid[abs(lastX-2)][abs(lastY-1)]:
            makeMove(abs(firstX-2),abs(firstY-1),COMPUTER)
        else:
            print "OPEN"
            empty = getOpen()
            print empty
            makeMove(empty[0],empty[1],COMPUTER)

        print totalMoves

        if totalMoves == 9:
            print "Its a DRAW!"

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 410, 261)
        self.setWindowTitle("Tic Tac Toe")
        self.setWindowIcon(QIcon('t3-icon.png'))

        dim_y = 30
        for i in range(3):
            dim_x = 30
            for j in range(3):
                cell[i].append(Cell(self,i,j,dim_x,dim_y,61,61))
                dim_x += 70

            dim_y+=70

        self.divider = QFrame(self)
        self.divider.setFrameStyle(QFrame.VLine)
        self.divider.setFrameShadow(QFrame.Sunken)
        self.divider.setGeometry(240,30,20,201)

        self.player_label = QLabel("Player :", self)
        self.player_label.setGeometry(270,30,61,21)
        self.player_symbol = QLabel(PLAYER,self)
        self.player_symbol.setStyleSheet("color:"+color[PLAYER]+"; font-size:14pt; font-weight:700")
        self.player_symbol.setGeometry(370,30,21,21)

        self.computer_label = QLabel("Computer :", self)
        self.computer_label.setGeometry(270,60,91,21)
        self.computer_symbol = QLabel(COMPUTER,self)
        self.computer_symbol.setStyleSheet("color:"+color[COMPUTER]+"; font-size:14pt; font-weight:700")
        self.computer_symbol.setGeometry(370,60,21,21)

        self.btn_quit = self.createButton("Quit",270,200,111,27)
        self.btn_new = self.createButton("New Game",270,170,111,27)
        self.btn_start = self.createButton("START",270,140,111,27)

        self.setButtonActions()
        self.show()

    def createButton(self, text, offset_x,offset_y,dim_x,dim_y):
        btn = QPushButton(text, self)
        btn.setGeometry(offset_x,offset_y,dim_x,dim_y)
        return btn

    def setButtonActions(self):
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_new.clicked.connect(self.resetAll)

    def resetAll(self):
        for row in cell:
            for c in row:
                c.reset()

        for row in grid:
            for x in row:
                x = ""

app = QApplication(sys.argv)
GUI = Window()
lastX = random.choice([0,2])
lastY = random.choice([0,2])
firstX = lastX
firstY = lastY
grid[lastX][lastY] = COMPUTER
cell[lastX][lastY].changeTo(COMPUTER)
sys.exit(app.exec_())
