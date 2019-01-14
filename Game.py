#!/usr/bin/python3

import sys
from time import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
from random import *
from Block import Block
from GameGrid import GameGrid
from Countdown import Countdown
import Backup

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p=self.palette()
        p.setColor(QPalette.Window, QColor(255 ,255 ,255))
                
class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()
        self.timeHs = 0
        self.timeS = 0
        self.finish = False
        self.currentLvl = 1
        self.interLevel = True
        self.initGrid(4,4)
        self.loadLevel()
        
    def initGrid(self,col,row):
        self.grid = GameGrid(col,row)
        self.adaptBlocks()
        self.new = Block(0,0,0,0,0,0,0)
        self.run=False
        self.end=False
        self.countdown = Countdown(6)
    
    def initUI(self):
        desktop = QDesktopWidget()
        screen = desktop.availableGeometry()
        self.setFixedSize(screen.height()/1.2,screen.height()/1.2)
        self.setWindowTitle('Editeur de niveau')
        self.setCenter()
        self.show()

    def closeEvent(self,event):
        sys.exit(Application)

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self,event):
        painter = QPainter(self)

        #Affichage de la grille
        painter.setBrush(QBrush(QColor(210, 210, 210)))
        painter.setPen(QPen(QColor(255, 255, 255)))
        for i in range(self.row):
            for j in range(self.col):
                rect = QRect(   self.verticalSpace + (self.blockSize + self.verticalSpace) * j,
                                self.horizontalSpace + (self.blockSize + self.horizontalSpace) * i,
                                self.blockSize,
                                self.blockSize)
                painter.drawRect(rect)

        #Affichage du nouveau block
        if self.new.size!=0:
            n=self.new
            s=self.new.size
        
            rectNew1 = QRect(   n.posColCurrent+(self.blockSize-s)/2,
                                n.posRowCurrent+(self.blockSize-s)/2,
                                s+self.verticalSpace*2,
                                s+self.horizontalSpace*2)
        
            rectNew2 = QRect(   n.posColCurrent+(self.blockSize-s)/2 + self.verticalSpace,
                                n.posRowCurrent+(self.blockSize-s)/2 + self.horizontalSpace,
                                s,
                                s)

            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawRect(rectNew1)
            painter.setBrush(QBrush(QColor(n.color)))
            painter.drawRect(rectNew2)

        #Affichage des blocks
        for b in self.blocks:
            rect1 = QRect(  b.posColCurrent,
                            b.posRowCurrent,
                            b.size+self.verticalSpace*2,
                            b.size+self.horizontalSpace*2)
            rect2 = QRect(b.posColCurrent+self.verticalSpace,b.posRowCurrent+self.horizontalSpace,b.size,b.size)
            painter.setPen(QPen(QColor(255,255,255)))
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawRect(rect1)
            painter.setBrush(QBrush(QColor(b.color)))
            painter.drawRect(rect2)
            font = QFont("Arial", 160/self.row, QFont.Bold)
            painter.setFont(font)
            if b.valeur>2:
                painter.setPen(QPen(QColor(255,255,255)))
                painter.drawText(rect1, Qt.AlignCenter, str(b.valeur))
            elif b.valeur>0:
                painter.setPen(QPen(QColor(76,76,76)))
                painter.drawText(rect1, Qt.AlignCenter, str(b.valeur))
        
        #Affichage des murs
        for m in self.grid.walls:
            rect = QRect(   (self.verticalSpace+self.blockSize)*m[1]+self.verticalSpace,
                            (self.horizontalSpace+self.blockSize)*m[0]+self.horizontalSpace,
                            self.blockSize,
                            self.blockSize)
            painter.setPen(QPen(QColor(255,255,255)))
            painter.setBrush(QBrush(QColor(69, 68, 69)))
            painter.drawRect(rect)

        #Affichage du coutdown
        rectTimer = QRect(self.width()-125,25,100,50)
        painter.setPen(QPen(QColor(255,255,255,150)))
        painter.setBrush(QBrush(QColor(255, 255, 255, 150)))
        painter.drawRect(rectTimer)
        font = QFont("Arial", 30, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor(76,76,76)))
        if self.countdown.hs < 9.9999:
            painter.drawText(rectTimer, Qt.AlignCenter,str(self.countdown.s)+".0"+str(self.countdown.hs))
        else:
            painter.drawText(rectTimer, Qt.AlignCenter,str(self.countdown.s)+"."+str(self.countdown.hs))

        #Affichage écran countdown écoulé
        if not self.countdown.runCount and not self.interLevel:
            rectEnd = QRect(0,0,self.width(),self.height())
            painter.setPen(QPen(QColor(76,76,76)))
            painter.setBrush(QBrush(QColor(255, 255, 255, 180)))
            painter.drawRect(rectEnd)
            font = QFont("Arial", 60, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rectEnd, Qt.AlignCenter, "Timed out!\n\n")
            font = QFont("Arial", 30, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rectEnd, Qt.AlignCenter, "\n\npress enter to retry")


        #Affichage écran win
        if self.interLevel and not self.finish:
            rectEnd = QRect(0,0,self.width(),self.height())
            painter.setPen(QPen(QColor(76,76,76)))
            painter.setBrush(QBrush(QColor(255, 255, 255, 180)))
            painter.drawRect(rectEnd)
            font = QFont("Arial", 60, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rectEnd, Qt.AlignCenter, "Level "+str(self.currentLvl)+"\n\n")
            font = QFont("Arial", 30, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rectEnd, Qt.AlignCenter, "\n\npress enter to start")

        #Affichage écran fin
        if self.finish:
            rectEnd = QRect(0,0,self.width(),self.height())
            painter.setPen(QPen(QColor(76,76,76)))
            painter.setBrush(QBrush(QColor(255, 255, 255, 180)))
            painter.drawRect(rectEnd)
            font = QFont("Arial", 40, QFont.Bold)
            painter.setFont(font)
            painter.drawText(rectEnd, Qt.AlignCenter, "Great you finished the game!\n\n")
            font = QFont("Arial", 18, QFont.Bold)
            painter.setFont(font)
            if self.timeHs < 9.9999:
                painter.drawText(rectEnd, Qt.AlignCenter,"\n\nYou have finished the game in "+str(self.timeS)+".0"+str(self.timeHs)+" seconds")
            else:
                painter.drawText(rectEnd, Qt.AlignCenter,"\n\nYou have finished the game in "+str(self.timeS)+"."+str(self.timeHs)+" seconds")
            if self.scoreHs < 9.9999:
                painter.drawText(rectEnd, Qt.AlignCenter,"\n\n\n\nBest score "+str(self.scoreS)+".0"+str(self.scoreHs)+" seconds")
            else:
                painter.drawText(rectEnd, Qt.AlignCenter,"\n\n\n\nBest score "+str(self.scoreS)+"."+str(self.scoreHs)+" seconds")


    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            #---Entrée---#
            if event.key() == Qt.Key_Return and not self.run:
                if self.finish:
                    self.close()
                self.loadLevel()
                self.countdown = Countdown(6)
                self.countdown.start()
                self.countdown.timer.timeout.connect(self.update)
                self.countdown.timer.timeout.connect(self.addTime)
                self.interLevel = False


            if self.countdown.runCount:
                #---Droite---#
                if event.key() == Qt.Key_Right and not self.run:
                    self.run = True
                    self.new.size=0
                    move = self.grid.moveRight()
                    self.adaptBlocks()
                    self.animationRight()
                    #if move :
                    #    self.new = self.adaptOneBlock(self.grid.addRandomBlock())
                    #    self.animationNew159()
                    #    self.adaptBlocks()

                #---Gauche---#
                elif event.key() == Qt.Key_Left and not self.run:
                    self.run = True
                    self.new.size=0
                    move = self.grid.moveLeft()
                    self.adaptBlocks()
                    self.animationLeft()
                    #if move :
                    #    self.new = self.adaptOneBlock(self.grid.addRandomBlock())
                    #    self.animationNew()
                    #    self.adaptBlocks()

                #---Bas---#
                elif event.key() == Qt.Key_Down and not self.run:
                    self.run = True
                    self.new.size=0
                    move = self.grid.moveDown()
                    self.adaptBlocks()
                    self.animationDown()
                    #if move :
                    #    self.new = self.adaptOneBlock(self.grid.addRandomBlock())
                    #    self.animationNew()
                    #    self.adaptBlocks()

                #---Haut---#
                elif event.key() == Qt.Key_Up and not self.run:
                    self.run = True
                    self.new.size=0
                    move = self.grid.moveUp()
                    self.adaptBlocks()
                    self.animationUp()
                    #if move :
                    #    self.new = self.adaptOneBlock(self.grid.addRandomBlock())
                    #    self.animationNew()
                    #    self.adaptBlocks()

            #self.end = self.grid.verifEnd()
            self.update()               
            QApplication.processEvents()
            if self.grid.verifWin():
                self.win()

    def mousePressEvent(self,event):
        if type(event) == QMouseEvent and not self.run:
            #---Clique droit---#
            if event.button() == Qt.RightButton:
                pass
            #---Clique gauche---#
            elif event.button() == Qt.LeftButton:
                pass
            self.update()               
            QApplication.processEvents()    

    def animationNew(self):
        self.run = True
        while self.new.size<self.blockSize:
            self.new.size+=self.blockSize/8
            self.update()
            QApplication.processEvents()
            sleep(0.01)
        self.new.size=self.blockSize
        self.run = False

    def animationRight(self):
        while self.run:
            compteur=0
            for i in range(len(self.blocks)):   #Boucle qui parcours les blocks
                self.blocks[i].posColCurrent+=self.blocks[i].speed*self.speed
                if  self.blocks[i].posColCurrent>=self.blocks[i].posColToReach:
                    compteur+=1
                    self.blocks[i].posColCurrent=self.blocks[i].posColToReach
            if compteur==len(self.blocks):
                self.run = False
            self.update()               
            QApplication.processEvents()
            sleep(0.01)

    def animationLeft(self):
        while self.run:
            compteur=0
            for i in range(len(self.blocks)):   #Boucle qui parcours les blocks
                self.blocks[i].posColCurrent-=self.blocks[i].speed*self.speed
                if  self.blocks[i].posColCurrent<=self.blocks[i].posColToReach:
                    compteur+=1
                    self.blocks[i].posColCurrent=self.blocks[i].posColToReach
            if compteur==len(self.blocks):
                self.run = False
            self.update()               
            QApplication.processEvents()
            sleep(0.01)

    def animationDown(self):
        while self.run:
            compteur=0
            for i in range(len(self.blocks)):   #Boucle qui parcours les blocks
                self.blocks[i].posRowCurrent+=self.blocks[i].speed*self.speed
                if  self.blocks[i].posRowCurrent>=self.blocks[i].posRowToReach:
                    compteur+=1
                    self.blocks[i].posRowCurrent=self.blocks[i].posRowToReach
            if compteur==len(self.blocks):
                self.run = False
            self.update()               
            QApplication.processEvents()
            sleep(0.01)

    def animationUp(self):
        while self.run:
            compteur=0
            for i in range(len(self.blocks)):   #Boucle qui parcours les blocks
                self.blocks[i].posRowCurrent-=self.blocks[i].speed*self.speed
                if  self.blocks[i].posRowCurrent<=self.blocks[i].posRowToReach:
                    compteur+=1
                    self.blocks[i].posRowCurrent=self.blocks[i].posRowToReach
            if compteur==len(self.blocks):
                self.run = False
            self.update()               
            QApplication.processEvents()
            sleep(0.01)

    def adaptBlocks(self):
        self.row = len(self.grid.matrix)
        self.col = len(self.grid.matrix[0])
        self.speed=18
        self.verticalSpace = 50/(self.col+1)
        self.horizontalSpace = 50/(self.row+1)
        self.blockSize = (self.width()-50)/self.col 
        self.blocks=[]
        b = self.grid.blocks
        for i in range(len(b)):
            self.blocks.append(self.adaptOneBlock(b[i]))

    def adaptOneBlock(self,b):
        return Block(   b.valeur,
                        (self.verticalSpace+self.blockSize)*b.posColToReach,
                        (self.horizontalSpace+self.blockSize)*b.posRowToReach,
                        (self.verticalSpace+self.blockSize)*b.posColCurrent,
                        (self.horizontalSpace+self.blockSize)*b.posRowCurrent,
                        b.speed,
                        self.blockSize*b.size)

    def win(self):
        if self.currentLvl < 15:
            self.currentLvl += 1
            self.interLevel = True
            self.loadLevel()
            self.countdown.stop()
            self.update()
        else:
            self.countdown.pause()
            self.saveScore()

    def addTime(self):
        self.timeHs += 1
        if self.timeHs >= 100:
            self.timeS += self.timeHs//100
            self.timeHs = self.timeHs%100

    def loadLevel(self):
        fileName = "niv"+str(self.currentLvl)
        data = Backup.load(fileName)
        self.grid = data["grid"]
        self.adaptBlocks()
        self.update()

    def saveScore(self):
        try:
            data = Backup.load("bestScore")
            self.scoreS = data["scoreS"]
            self.scoreHs = data["scoreHs"]
            if self.timeS < self.scoreS or (self.timeS == self.scoreS and self.timeHs < self.scoreHs):
                Backup.saveScore("bestScore",self.timeS,self.timeHs)
        except:
            Backup.saveScore("bestScore",self.timeS,self.timeHs)
            data = Backup.load("bestScore")
        data = Backup.load("bestScore")
        self.scoreS = data["scoreS"]
        self.scoreHs = data["scoreHs"]
        self.finish = True
        self.update()