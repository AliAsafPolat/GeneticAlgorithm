# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 11:36:16 2021

@author: Asaf
"""
import random
import math
import numpy as np

# Verilen vektorun unit vector halini verir.
def unitVector(vector):
    return vector / np.linalg.norm(vector)

# Verilen vektorler arasindaki aciyi verir.
def getAngleBetweenVectors(v1, v2):
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    return math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))) % 360

# Verilen iki nokta arasindeki aci bilgisini verir.
def getVector(x1, y1, x2, y2):
    dX = x2 - x1
    dY = y2 - y1
    return (dX, dY)

# 9x9 luk alanda rastgele (x,y) koordinat degerleri uretip verir.
def createSeed(seedUzunlugu):
    createdSeed = []
    createdSeed.append((0,0))
    for i in range(seedUzunlugu):
        x = random.randint(0,8)
        y = random.randint(0,8)
        createdSeed.append((x,y))
    createdSeed.append((0,0))
    return createdSeed

if __name__ == '__main__':
    x = createSeed(10)
    
    v1 = getVector(0,0,1,1)
    v2 = getVector(1,1,0,1)
    aci = getAngleBetweenVectors(v1,v2)    
    print(x)
    print(aci)
        