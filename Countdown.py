#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Countdown():
    def __init__(self,s):
        self.s = s
        self.hs = 0
        self.runCount = False
        self.inPause = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.countdown)

    def start(self):
        self.runCount = True
        self.inPause = False
        self.timer.start(10)

    def stop(self):
        self.timer.stop()
        self.runCount = False

    def pause(self):
        self.timer.stop()
        self.inPause = True

    def countdown(self):
        if self.s <= 0 and self.hs <= 0:
            self.stop()
        elif self.hs <= 0:
            self.s -= 1
            self.hs = 99
        if self.hs > 0:
            self.hs -= 1


