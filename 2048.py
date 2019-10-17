import sys
import random

import math
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip,
                             QPushButton, QMessageBox,QDesktopWidget,
                             QLabel,QLineEdit,QTextEdit,QGridLayout,QInputDialog)
from PyQt5.QtGui import QIcon,QPainter,QBrush,QColor,QFont,QPixmap
from PyQt5.QtCore import Qt


class board:

    def __init__(self,x=4):
        
        self.init_val = [0,0,0,0,2,2,4]
        self.x = x
        
        self.value = [ [ random.choice(self.init_val) for i in range(self.x) ] for j in range(self.x) ] 

        
        self.failure = self.check_empty()[2]
        self.score = self.score_cal()


    def score_cal(self):
        maxim = self.value[0][0]
        for i in range(self.x):
            for j in range(self.x):
                if( self.value[i][j] > maxim ):
                    maxim = self.value[i][j]

        return maxim
       
    def calculator(self,direc):

        self.move(direc)
        if(direc == 'l'):
            for i in range(self.x):
                pos = self.x - 1
                while(pos > 0):
                    if( self.value[i][pos] == self.value[i][pos-1] and self.value[i][pos]!=0 ):
                        self.value[i][pos-1] = self.value[i][pos] * 2
                        self.value[i][pos]=0
                        self.move(direc)
                        pos =self.x - 1
                        
                    pos = pos - 1
                    
        if(direc == 'r'):
            for i in range(self.x):
                pos = 0
                while(pos < self.x-1):
                    if( self.value[i][pos] == self.value[i][pos+1] and self.value[i][pos]!=0 ):
                        self.value[i][pos+1] = self.value[i][pos] * 2
                        self.value[i][pos]=0
                        self.move(direc)
                        pos = 0
                        
                    pos = pos + 1

        if(direc == 'u'):
            for i in range(self.x):
                pos = self.x-1
                while(pos > 0):
                    if( self.value[pos][i] == self.value[pos-1][i] and self.value[pos][i]!=0 ):
                        self.value[pos-1][i] = self.value[pos][i] * 2
                        self.value[pos][i]=0
                        self.move(direc)
                        pos = self.x - 1
                        
                    pos = pos - 1

        if(direc == 'd'):
            for i in range(self.x):
                pos = 0
                while(pos < self.x-1):
                    if( self.value[pos][i] == self.value[pos+1][i] and self.value[pos][i]!=0 ):
                        self.value[pos+1][i] = self.value[pos][i] * 2
                        self.value[pos][i]=0
                        self.move(direc)
                        pos = 0
                        
                    pos = pos + 1

        self.score = self.score_cal()
        self.num_generator()
        
    def move(self,direc):
        if(direc == 'l'):
            for i in range(self.x):
                temp1 = 0
                for temp2 in range(self.x):
                    if( self.value[i][temp2] != 0 ):
                        self.value[i][temp1] = self.value[i][temp2]
                        temp1 = temp1 + 1
                while(temp1<self.x):
                    self.value[i][temp1] = 0
                    temp1 = temp1 + 1

        if(direc == 'r'):
            for i in range(self.x):
                temp1 = self.x - 1
                for temp2 in range(self.x-1,-1,-1):
                    if( self.value[i][temp2] != 0 ):
                        self.value[i][temp1] = self.value[i][temp2]
                        temp1 = temp1 - 1
                while(temp1>=0):
                    self.value[i][temp1] = 0
                    temp1 = temp1 - 1            
                    
        if(direc == 'u'):
            for i in range(self.x):
                temp1 = 0
                for temp2 in range(self.x):
                    if( self.value[temp2][i] != 0 ):
                        self.value[temp1][i] = self.value[temp2][i]
                        temp1 = temp1 + 1
                while(temp1<self.x):
                    self.value[temp1][i] = 0
                    temp1 = temp1 + 1       
        
        if(direc == 'd'):
            for i in range(self.x):
                temp1 = self.x - 1
                for temp2 in range(self.x-1,-1,-1):
                    if( self.value[temp2][i] != 0 ):
                        self.value[temp1][i] = self.value[temp2][i]
                        temp1 = temp1 - 1
                while(temp1>=0):
                    self.value[temp1][i] = 0
                    temp1 = temp1 - 1  

    def check_empty(self):
        
        l1 = []; l2 = []
        for i in range(self.x):
            for j in range(self.x):
                if(self.value[i][j]==0):
                    l1.append(i)
                    l2.append(j)
                    
        return l1,l2,len(l1)==0

    def num_generator(self):

        l1,l2,full_or_not = self.check_empty()
        if(full_or_not != True):
            n = max(1,int(len(l1)/5))
            index = random.sample( range(len(l1)),n )
            for i in index:
                self.value[l1[i]][l2[i]] = random.choice([2,2,2,2,4,4,8])

        else:
            self.failure = True

class ui(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        self.setToolTip("A game aimed to get 2048")
               
        self.resize(600,600)
        self.center()
        self.height = self.height()
        self.width = self.width()

        
        
        self.x,ok = QInputDialog.getInt(self,"输入框","请输入每一行的方格数:",4,4,8,1)

        QMessageBox.information(self,"提示","请按下方向键进行操作。您需要获得数字1024,才能取得胜利!")

        
        self.setStyleSheet("QLabel{background-color:rgb(220,220,220);"
                   "border-style: outset;}"
                   "QLabel{color:rgb(100,100,100,250);font-size:45px;font-weight:bold;font-family:Roman times;}"
                   "QLabel:hover{color:rgb(100,100,100,120);}")


        self.board = board(self.x)
        
        self.lb = self.label_generator()

        self.drawNum()
        self.color_map()

        self.setWindowTitle('2048')
        self.setWindowIcon(QIcon('2048.png'))
        self.show()

        
    def label_generator(self):
        
        lb = [ [i for i in range(self.x)] for j in range(self.x) ]
        self.lb_inv = 5   # number of pixels between two adjacent QLabel
        self.lb_width = int( (self.width-30-self.lb_inv*(self.x-1))/self.x )
        self.lb_height = int( (self.height-30-self.lb_inv*(self.x-1))/self.x )

        for i in range(self.x):
            for j in range(self.x):
                lb[i][j] = QLabel(str(self.board.value[i][j]),self)
                lb[i][j].setGeometry(15+(self.lb_width+self.lb_inv)*j,15+(self.lb_height+self.lb_inv)*i,self.lb_width,self.lb_height)
                lb[i][j].setAlignment(Qt.AlignCenter)
        return lb

    # remove attached labels from the window
    def remove_label(self):
        for i in range(self.x):
            for j in range(self.x):
                self.lb[i][j].setParent(None)
        return None
              
    def drawNum(self):
        for i in range(self.x):
            for j in range(self.x):
                if(self.board.value[i][j] == 0):
                    self.lb[i][j].setText('')
                else:    
                    self.lb[i][j].setText(str(self.board.value[i][j]))
                
        return None
        

    def color_map(self):
        
        color = [ "#4682B4","#00CED1","#FF1493","#FFA500","#8B3626","#8B0000","#FF8247","#FFA500","#FF4500","#FF0000"]
        # another combination of colors
        # color = [ "#E1F5FE","#B3E5FC","#81D4FA","#4FC3F7","#29B6F6","#03A9F4","#039BE5","0288D1","0277BD","01579B"]
        
        for i in range(self.x):
            for j in range(self.x):
                if( self.board.value[i][j] >= 2 and self.board.value[i][j] <= 1024 ):
                    self.lb[i][j].setStyleSheet("color:"+ color[int(math.log(self.board.value[i][j],2))-1]+";")
                else:
                    self.lb[i][j].setStyleSheet("color:#323232;")

        return None
    
    def center(self):       
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        return None
        

    def keyPressEvent(self,event):

        key = event.key()
        if(key == Qt.Key_Left):
            self.board.calculator('l')
        if(key == Qt.Key_Right):
            self.board.calculator('r')
        if(key == Qt.Key_Up):
            self.board.calculator('u')
        if(key == Qt.Key_Down):
            self.board.calculator('d')

        self.drawNum()
        self.color_map()
        
        if(self.board.score == 1024):
            reply = QMessageBox.question(self,
                                    "打得不错!",  
                                    "你赢了,但这个世界已经在劫难逃..是否重来?",  
                                    QMessageBox.Yes | QMessageBox.No)
            if(reply == QMessageBox.Yes):
                self.board = board(self.x)
                self.drawNum()
                self.color_map()
                

        elif(self.board.failure == True):
            reply = QMessageBox.question(self,
                                    "哦,糟了!",  
                                    "发生这种事我很抱歉...是否重来?",  
                                    QMessageBox.Yes | QMessageBox.No)
            if(reply == QMessageBox.Yes):
                self.board = board(self.x)
                self.drawNum()
                self.color_map()
                
                
        return None     


        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = ui()
    
    sys.exit(app.exec_())
