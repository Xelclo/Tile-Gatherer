#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from Block import Block

class GameGrid():
    def __init__(self,col,row):
        self.matrix=[]
        self.blocks=[]
        self.walls=[]
        self.row=row
        self.col=col
        for i in range(self.row):
            self.matrix.append([])
            for j in range(self.col):
                self.matrix[i].append(1)
        self.addRandomBlock()

    def addRandomBlock(self):
        while True:
            i=randint(0,self.row-1)
            j=randint(0,self.col-1)
            if self.matrix[i][j]==1:
                num=randint(0,7)
                if num>=7:
                    self.matrix[i][j]=4
                else:
                    self.matrix[i][j]=2
                break
        self.refreshVar()
        return Block(self.matrix[i][j], 0, 0, j, i, 0, 0)

    def addBlock(self,j,i):
        if self.matrix[i][j]==1:
            self.matrix[i][j]=2
        elif self.matrix[i][j] not in {0,1}:
            self.matrix[i][j]=1
        self.refreshVar()
        return Block(self.matrix[i][j], 0, 0, j, i, 0, 0)
        

    def addWall(self,j,i):
        if self.matrix[i][j]==1:
            self.matrix[i][j]=0
        elif self.matrix[i][j]==0:
            self.matrix[i][j]=1
        self.refreshVar()

    def addSupportBlock(self,j,i):
        if self.matrix[i][j]==1:
            self.matrix[i][j]=-1
        elif self.matrix[i][j] < 0:
            self.matrix[i][j]=1
        self.refreshVar()
        return Block(self.matrix[i][j], 0, 0, j, i, 0, 0)
    
    def verifEnd(self):
        end=True
        for i in range(self.row):
            if not end:
                break
            for j in range(self.col):
                if self.matrix[i][j]==1:
                    end=False
                    break
                if i>0 and self.matrix[i][j]!=0 and self.matrix[i][j]==self.matrix[i-1][j]:
                    end=False
                    break
                if i<self.row-1 and self.matrix[i][j]!=0 and self.matrix[i][j]==self.matrix[i+1][j]:
                    end=False
                    break
                if j>0 and self.matrix[i][j]!=0 and self.matrix[i][j]==self.matrix[i][j-1]:
                    end=False
                    break
                if j<self.col-1 and self.matrix[i][j]!=0 and self.matrix[i][j]==self.matrix[i][j+1]:
                    end=False
                    break
        return end

    def verifWin(self):
        win=True
        k=0
        for i in range(self.row):
            if not win:
                break
            for j in range(self.col):
                if self.matrix[i][j]>1:
                    k+=1
                    if k>1:
                        win = False
                        break
        return win

    def refreshVar(self):
        self.blocks=[]
        self.walls=[]
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] not in {0,1}:
                    self.blocks.append(Block(self.matrix[i][j], 0, 0, j, i, 0, 1))
                elif self.matrix[i][j] == 0:
                    self.walls.append((i,j))

    def moveRight(self):
        listFusion=[]
        self.blocks=[]
        move=False
        for i in range(self.row):
            for j in range(self.col-1,-1,-1):
                if self.matrix[i][j] not in {0,1}:
                    compteur=0
                    k=j
                    while k+1<self.col and self.matrix[i][k+1]==1:
                        self.matrix[i][k+1]=self.matrix[i][k]
                        self.matrix[i][k]=1
                        k+=1
                        compteur+=1
                        move=True
                    if k+1<self.col and self.matrix[i][k+1]==self.matrix[i][k] and (i,k+1) not in listFusion and self.matrix[i][k]>0:
                        self.matrix[i][k+1]=self.matrix[i][k]*2
                        self.matrix[i][k]=1
                        k+=1
                        compteur+=1
                        listFusion.append((i,k))
                        move=True
                    self.blocks.append(Block(self.matrix[i][k], k, i, j, i, compteur, 1))
        return move

    def moveLeft(self):
        listFusion=[]
        self.blocks=[]
        move=False
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] not in {0,1}:
                    compteur=0
                    k=j
                    while k-1>=0 and self.matrix[i][k-1]==1:
                        self.matrix[i][k-1]=self.matrix[i][k]
                        self.matrix[i][k]=1
                        k-=1
                        compteur+=1
                        move=True
                    if k-1>=0 and self.matrix[i][k-1]==self.matrix[i][k] and (i,k-1) not in listFusion and self.matrix[i][k]>0:
                        self.matrix[i][k-1]=self.matrix[i][k]*2
                        self.matrix[i][k]=1
                        k-=1
                        compteur+=1
                        listFusion.append((i,k))
                        move=True
                    self.blocks.append(Block(self.matrix[i][k], k, i, j, i, compteur, 1))
        return move

    def moveDown(self):
        listFusion=[]
        self.blocks=[]
        move=False
        for i in range(self.row-1,-1,-1):
            for j in range(self.col):
                if self.matrix[i][j] not in {0,1}:
                    compteur=0
                    k=i
                    while k+1<self.row and self.matrix[k+1][j]==1:
                        self.matrix[k+1][j]=self.matrix[k][j]
                        self.matrix[k][j]=1
                        k+=1
                        compteur+=1
                        move=True
                    if k+1<self.row and self.matrix[k+1][j]==self.matrix[k][j] and (k+1,j) not in listFusion and self.matrix[k][j]>0:
                        self.matrix[k+1][j]=self.matrix[k][j]*2
                        self.matrix[k][j]=1
                        k+=1
                        compteur+=1
                        listFusion.append((k,j))
                        move=True
                    self.blocks.append(Block(self.matrix[k][j], i, k, j, i, compteur, 1))
        return move

    def moveUp(self):
        listFusion=[]
        self.blocks=[]
        move=False
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] not in {0,1}:
                    compteur=0
                    k=i
                    while k-1>=0 and self.matrix[k-1][j]==1:
                        self.matrix[k-1][j]=self.matrix[k][j]
                        self.matrix[k][j]=1
                        k-=1
                        compteur+=1
                        move=True
                    if k-1>=0 and self.matrix[k-1][j]==self.matrix[k][j] and (k-1,j) not in listFusion and self.matrix[k][j]>0:
                        self.matrix[k-1][j]=self.matrix[k][j]*2
                        self.matrix[k][j]=1
                        k-=1
                        compteur+=1
                        listFusion.append((k,j))
                        move=True
                    self.blocks.append(Block(self.matrix[k][j], i, k, j, i, compteur, 1))
        return move