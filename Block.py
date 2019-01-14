#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Block():
    def __init__(self, valeur, posColToReach, posRowToReach, posColCurrent, posRowCurrent, speed, size):
        self.valeur = valeur
        self.posColToReach = posColToReach
        self.posRowToReach = posRowToReach
        self.posColCurrent = posColCurrent
        self.posRowCurrent = posRowCurrent
        self.speed = speed
        self.size = size
        if valeur==2:
            #self.color=QColor(238,228,218)
            self.color=QColor(245,242,220)
        elif valeur==4:
            #self.color=QColor(237,224,200)
            self.color=QColor(140,209,199)
        elif valeur==8:
            #self.color=QColor(242,177,121)
            self.color=QColor(0,148,148)
        elif valeur==16:
            #self.color=QColor(236,141,84)
            self.color=QColor(0,88,94)
        elif valeur==32:
            self.color=QColor(246,124,95)
        elif valeur==64:
            self.color=QColor(234,89,55)
        elif valeur==128:
            self.color=QColor(243,216,107)
        elif valeur==256:
            self.color=QColor(241,208,75)
        elif valeur==512:
            self.color=QColor(228,192,42)
        elif valeur==1024:
            self.color=QColor(226,186,19)
        elif valeur<0:
            #self.color=QColor(159,243,214)
            self.color=QColor(255,87,41)
        else:
            #self.color=QColor(0,0,0)
            self.color=QColor(69,68,69)