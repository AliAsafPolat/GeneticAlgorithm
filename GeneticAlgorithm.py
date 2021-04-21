# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 11:36:16 2021

@author: Asaf
"""
import random
import math
import numpy as np
from numpy.random import choice
from decimal import *


class FitnessIdx:
    def __init__(self, idx, fitness):
        self.idx = idx
        self.fitness = fitness
        self.prob = 0
        
    def setProbablity(self, probablity):
        self.prob = probablity
        

# Verilen vektorun unit vector halini verir.
def unitVector(vector):
    return vector / np.linalg.norm(vector)

# Verilen vektorler arasindaki aciyi verir.
def getAngleBetweenVectors(v1, v2):
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    # Sonucun normalize edilmis halini dondurur.
    return (math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))) % 360) / 360

# Verilen iki noktadan cizilen vektoru verir.
def getVector(x1, y1, x2, y2):
    dX = x2 - x1
    dY = y2 - y1
    return (dX, dY)

# 9x9 luk alanda rastgele yön degerleri uretip verir.
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

# Dronelarin ne kadar adimlik gezinimler yapacagi bilgisini dondurur.
def getPathLengthPerDrone(droneCount, width, height):
    fieldCount = width * height
    return math.ceil((fieldCount - 1) / droneCount)    

# Olusturulan rotadaki koordinatlarin alan icerisinde olup ve birbirlerinden farkli olma sayisi 
def getDifferentPointsCountInTheField_Fitness(route):
    count = 0
    marked = []
    for point in route:
        if(marked.count(point)<1 and isInTheField(point,9,9,0,0)):
            count += 1
            marked.append(point)
    # Max fonksiyonu min fonksiyonuna cevirildi.
    return 1/count

# Bitis noktasi ile hedef nokta arasindaki Euclid Distance bilgisini verir.
def getFinalDistancesFromEndPoint_Fitness(finalPoint, endPoint):
    # Normalize edilmis sonuc doner.
    return math.sqrt(pow((finalPoint[0] - endPoint[0]),2) + pow((finalPoint[1] - endPoint[1]),2))/11.3
    #return (abs(finalPoint[0] - endPoint[0]) + abs(finalPoint[1] - endPoint[1])) / 10

# Verilen rotada olusturulan acilarin toplamini verir.
def getTurningAnglesInRoute_Fitness(route):
    angleRes = 0
    v0 = getVector(route[0][0],route[0][1],route[1][0],route[1][1])
    
    for i in range(2,len(route)):
        v1 = getVector(route[i-1][0],route[i-1][1], route[i][0], route[i][1])
        angle_ = getAngleBetweenVectors(v0,v1)
        #print("Turning Angle ", i , " : ", angle_)
        angleRes += angle_
        v0 = v1
    return angleRes

# Fitness fonksiyonlari toplanarak genel fitness sonucu dondurulur.
def getFitnessScore(route, finalPoint, endPoint):
    fitDiffPoint = getDifferentPointsCountInTheField_Fitness(route)
    fitFinalDist = getFinalDistancesFromEndPoint_Fitness(finalPoint, endPoint)
    fitTurningAng = getTurningAnglesInRoute_Fitness(route)
    return fitDiffPoint + fitFinalDist+ fitTurningAng

# Verilen class edemanin uygun degeri bilgisi geri dondurulur.
def takeFitnessScore(elem):
    return elem.fitness

# Verilen parentların genlerinden rastgele secilen bir yerden cross over islemi yapilir ve sonuclardan biri rastgele olarak dondurulur.
def applyCrossOver(parentX, parentY):
    kromLen = len(parentX)
    crossPoint = random.randint(0,kromLen)
    #print("Cross point : ", crossPoint)
    #parenX de 0 dan secilen noktaya kadar olan kisim parentY'ye
    
    
    tmp = parentX.copy()
    
    for i in range(crossPoint):
        parentX[i] = parentY[i]
        parentY[i] = tmp[i]
    
    
    if(crossPoint % 2 == 0):
        return parentX
    else:
        return parentY
    
# Populasyondaki kromozomlarin secim ihtimallerinin atamasini yapar.        
def setPopulationProbablities(population):
    totalProbablity = len(population) * len(population) / 2
    for i,krom in enumerate(population):
        krom.setProbablity((len(population) - i) / (totalProbablity))
    

# Verilen populasyon icerisinden secilme olasiliklarina gore rastgele secim yapar. 
# Alinan parametrede class listesi vardır. Elemanlarin fitness degerleri bu parametre icerisinde bulunmaktadir.
def randomSelection(population):
    probablities = []
    for i in range(len(population)):
        probablities.append(population[i].prob) # fitness degeri az olanın ihtimali cok olmasi gerek.
    
    selection = random.choices(population, probablities,k=1)
    # Secilen degerin hangi indisde bulundugu bilgisi dondurulur.
    #print("Selected fitness : ", selection[0].fitness)
    return selection[0].idx


def applyMutationProbablity(kromozom, mutationProbablity):
    
    for i in range(len(kromozom)):
        prob = random.uniform(0.0, 1.0)
        #print(prob)
        if(prob < mutationProbablity):
            kromozom[i] = random.randint(1,8)
        

if __name__ == '__main__':
    #droneCount = input("Enter Drone Count : ")
    
    populationCount = 1000
    mutationProbablity = 0.1
    startingPoint = endPoint = (0,0)
    population = []
    routes = []
    fitnessVals = []
    
    # Ilk populasyon olusturulur.
    for i in range(populationCount):
        population.append(createSeed(80))
        routes.append(seedToCoordinate(population[i], startingPoint))
        fitnessVals.append( FitnessIdx(i, getFitnessScore(routes[i], routes[i][-1], endPoint)))
    
    #print("Fitness : ", fitnessVals[0].fitness)
    fitnessVals.sort(key=takeFitnessScore)
            
    # Yapilan siralamaya gore populasyondaki kromozomlarin secilme olasiliklarini atar.
    setPopulationProbablities(fitnessVals)
    
    endCondition = True
    
    while endCondition:
        newPopulation = []
        newFitnessVals = []
        newRoutes = []
        for i in range(populationCount):
            parentX_Idx = randomSelection(fitnessVals)
            parentY_Idx = randomSelection(fitnessVals)
            
            parentX_kromozom = population[parentX_Idx]
            parentY_kromozom = population[parentY_Idx]
            
            # Fonksiyon icinde dizideki degerler degistiginden kopyasini gonderiyorum.
            child = applyCrossOver(parentX_kromozom.copy(), parentY_kromozom.copy())
            # Mutasyon ihtimalini ekler.
            applyMutationProbablity(child, mutationProbablity)        
            
            newPopulation.append(child)
            newRoutes.append(seedToCoordinate(child, startingPoint))
            newFitnessVals.append( FitnessIdx(i, getFitnessScore(newRoutes[i], newRoutes[i][-1], endPoint)))
    
            
            
        population = newPopulation
        routes = newRoutes
        fitnessVals = newFitnessVals
        fitnessVals.sort(key = takeFitnessScore)
        print("Fitness val : ", fitnessVals[0].fitness)
            
        if(fitnessVals[0].fitness < 1.5):
            endCondition = False
            print("Final fitness : ", fitnessVals[0].fitness)
            print("Final path : ", population[fitnessVals[0].idx])
        
    #print("Parent X : ", parentX_kromozom)
    #print("Parent Y : ", parentY_kromozom)
    #print("Child : ", child)
    
    
    