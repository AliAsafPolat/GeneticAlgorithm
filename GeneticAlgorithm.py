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

# Verilen iki noktadan cizilen vektoru verir.
def getVector(x1, y1, x2, y2):
    dX = x2 - x1
    dY = y2 - y1
    return (dX, dY)

# 9x9 luk alanda rastgele (x,y) koordinat degerleri uretip verir.
def createSeed(seedUzunlugu):
    createdSeed = []
    for i in range(seedUzunlugu):
        direction = random.randint(1,8)
        createdSeed.append(direction)
    return createdSeed

# Verilen baslangic noktasi ve yon bilgisine gore koordinatlari dondurur.
def seedToCoordinate(directionSeed, startingPoint):
    route = []
    route.append(startingPoint)
    point = startingPoint
    for direction in directionSeed:
        if(direction == 1):
            point = (point[0], point[1] + 1)
        elif(direction == 2):
            point = (point[0] - 1, point[1] + 1)
        elif(direction == 3):
            point = (point[0] - 1, point[1])
        elif(direction == 4):
            point = (point[0] - 1, point[1] - 1)
        elif(direction == 5):
            point = (point[0], point[1] - 1)
        elif(direction == 6):
            point = (point[0] + 1, point[1] - 1)
        elif(direction == 7):
            point = (point[0] + 1, point[1])
        elif(direction == 8):
            point = (point[0] + 1, point[1] + 1)
        else:
            print("Unvalid direction")
            break
        
        route.append(point)
    return route
            
# Verilen noktanın istenilen alan icerisinde olup olmadigi bilgisini dondurur.
def isInTheField(point, fieldWidth, fieldHeight, fieldStartingX, fieldStartingY):
    if(point[0] < fieldStartingX or point[0] >= fieldStartingX + fieldWidth or point[1] < fieldStartingY 
       or point[1] >= fieldStartingY + fieldHeight):
        return False
    else:
        return True

# Olusturulan rotadaki koordinatlarin alan icerisinde olup ve birbirlerinden farkli olma sayisi 
def getDifferentPointsCountInTheField(route):
    count = 0
    marked = []
    for point in route:
        if(marked.count(point)<1 and isInTheField(point,9,9,0,0)):
            count += 1
            marked.append(point)
    return count

# Bitis noktasi ile hedef nokta arasindaki Manhattan Distance bilgisini verir.
def getFinalDistancesFromEndPoint(finalPoint, endPoint):
    return abs(finalPoint[0] - endPoint[0]) + abs(finalPoint[1] - endPoint[1])

# Verilen rotada olusturulan acilarin toplamini verir.
def getTurningAnglesInRoute(route):
    angleRes = 0
    v0 = getVector(route[0][0],route[0][1],route[1][0],route[1][1])
    
    for i in range(2,len(route)):
        v1 = getVector(route[i-1][0],route[i-1][1], route[i][0], route[i][1])
        angle_ = getAngleBetweenVectors(v0,v1)
        print("Turning Angle ", i , " : ", angle_)
        angleRes += angle_
        v0 = v1
    return angleRes

if __name__ == '__main__':
    x = createSeed(10)
    
    v1 = getVector(0,0,1,1)
    v2 = getVector(1,1,0,1)
    aci = getAngleBetweenVectors(v1,v2)    
    print(x)
    
    #print(aci)
    
    route = seedToCoordinate(x, (0,0)) 
    for r in route:
        print(r)
    
    diffPointCount = getDifferentPointsCountInTheField(route)
    print("Different point count in the route : ", diffPointCount)    
    
    angleRes = getTurningAnglesInRoute(route)
    print("Angle addition res : ", angleRes)
    
    