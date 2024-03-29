import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random

global GUI

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
RESET = True
START = False

def getOpen():
    for i in range(3):
        for j in range(3):
            if not grid[i][j]:
                return [i,j]

def checkTwoPair(value):

    for i in range(3):
        if grid[i].count(value)==2 and grid[i].count('')==1:
            return [i,grid[i].index('')]

    for i in range(3):
        col = [grid[0][i],grid[1][i],grid[2][i]]
        if col.count(value)==2 and col.count('')==1:
            return [col.index(''),i]

    diag1 = [grid[0][0],grid[1][1],grid[2][2]]
    if diag1.count(value)==2 and diag1.count('')==1:
        return [diag1.index(''),diag1.index('')]

    diag2 = [grid[0][2],grid[1][1],grid[2][0]]
    if diag2.count(value)==2 and diag2.count('')==1:
        return [diag2.index(''),abs(diag2.index('')-2)]

    return False

def makeMove(i,j,value):
    global grid,cell
    grid[i][j] = value
    cell[i][j].changeTo(value)

def makeFirstMove():
    global RESET,START,lastX,lastY,firstX,firstY,cell

    for i in range(3):
        for j in range(3):
            cell[i][j].set = False

    START = True

    if RESET:
        lastX = random.choice([0,2])
        lastY = random.choice([0,2])
        firstX = lastX
        firstY = lastY
        makeMove(lastX,lastY,COMPUTER)
        RESET = False
    else:
        return

def displayResult(title,message):
    GUI.showMessage(title,message)

class Cell(QLabel):

    def __init__(self,win,a,b,offset_x,offset_y,dim_x,dim_y):
        self.i = a
        self.j = b
        self.set = True
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
            return

    def reset(self):
        self.label.setStyleSheet("background-color:#CCC;")
        self.label.setText("")
        self.label.setCursor(QCursor(Qt.PointingHandCursor))
        self.set = False

    def clicked(self,event):
        global lastX, lastY, cell, START

        if not START:
            displayResult("Alert","Press \"START\" to begin")
            return

        if self.set:
            return

        self.changeTo(PLAYER)

        lastX = self.i
        lastY = self.j

        if checkTwoPair(COMPUTER):
            winPos = checkTwoPair(COMPUTER)
            makeMove(winPos[0],winPos[1],COMPUTER)
            displayResult("Game Over","Computer WINS!")

        elif checkTwoPair(PLAYER):
            newPos = checkTwoPair(PLAYER)
            makeMove(newPos[0],newPos[1],COMPUTER)

        elif not grid[1][1] and [lastX,lastY] in sides:
            makeMove(1,1,COMPUTER)

        elif [lastX,lastY] == [1,1]:
            makeMove(abs(firstX-2),abs(firstY-2),COMPUTER)

        elif [lastX,lastY] in corners and  not grid[abs(lastX-2)][abs(lastY-2)]:
            if COMPUTER in grid[lastX]:
                makeMove(abs(lastX-1),abs(lastY-2),COMPUTER)
            else:
                makeMove(abs(lastX-2),abs(lastY-1),COMPUTER)

        elif [lastX,lastY] == [abs(firstX-2),abs(firstY-2)] and not grid[1][1]:
            makeMove(1,1,COMPUTER)

        elif not grid[abs(lastX-1)][abs(lastY-2)]:
            makeMove(abs(lastX-1),abs(lastY-2),COMPUTER)

        elif not grid[abs(lastX-2)][abs(lastY-1)]:
            makeMove(abs(lastX-2),abs(lastY-1),COMPUTER)

        else:
            empty = getOpen()
            makeMove(empty[0],empty[1],COMPUTER)

        if totalMoves == 9:
            displayResult("Game Over","Its a DRAW!")

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 410, 261)
        self.setWindowTitle("Tic Tac Toe")
        app_icon = QIcon()
        app_icon.addFile('icons/t3-icon.png',QSize(1042,1042))
        self.setWindowIcon(app_icon)

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

        self.player_label = self.createLabel("Player :",270,30,61,21)
        self.player_symbol = self.createLabel(PLAYER,370,30,21,21,"color:"+color[PLAYER]+"; font-size:14pt; font-weight:700")
        self.computer_label = self.createLabel("Computer :",270,60,91,21)
        self.computer_symbol = self.createLabel(COMPUTER,370,60,21,21,"color:"+color[COMPUTER]+"; font-size:14pt; font-weight:700")

        self.btn_quit = self.createButton("Quit",270,200,111,27)
        self.btn_new = self.createButton("New Game",270,170,111,27)
        self.btn_start = self.createButton("START",270,140,111,27)

        self.setButtonActions()
        self.show()

    def createLabel(self,name,x,y,l,b,style=""):
        label = QLabel(name,self)
        label.setGeometry(x,y,l,b)
        if style:
            label.setStyleSheet(style)
        return label

    def createButton(self, text, offset_x,offset_y,dim_x,dim_y):
        btn = QPushButton(text, self)
        btn.setGeometry(offset_x,offset_y,dim_x,dim_y)
        return btn

    def setButtonActions(self):
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_new.clicked.connect(self.resetAll)
        self.btn_start.clicked.connect(makeFirstMove)

    def showMessage(self,title,message):
        choice = QMessageBox.information(self, title, message, QMessageBox.Ok)
        if choice == QMessageBox.Ok:
            self.resetAll()

    def resetAll(self):
        global RESET,START,totalMoves,grid,cell

        for i in range(3):
            for j in range(3):
                cell[i][j].reset()
                grid[i][j] = ''

        RESET = True
        START = False
        totalMoves = 0

app = QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
