#!/usr/bin/python3

import pickle

def save(fileName,grid):
    data = {}
    data["grid"] = grid
    s = pickle.dumps(data)
    f = open(fileName,"wb")
    f.write(s)
    f.close()

def saveScore(fileName,scoreS,scoreHs):
    data = {}
    data["scoreS"] = scoreS
    data["scoreHs"] = scoreHs
    s = pickle.dumps(data)
    f = open(fileName,"wb")
    f.write(s)
    f.close()
    
def load(fileName):
    f = open(fileName,"rb")
    data = pickle.loads(f.read())
    return data