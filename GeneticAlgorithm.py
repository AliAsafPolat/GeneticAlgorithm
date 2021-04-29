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
import matplotlib.pyplot as plt

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
    if((v1[0] == 0 and v1[1] == 0) or (v2[0] == 0 and v2[1] == 0) ):
        return None
    #print("V1 : ", v1, " ** V2 : ", v2)
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    # Sonucun normalize edilmis halini dondurur.
    return (math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))) % 360) / 360

# Verilen iki noktadan cizilen vektoru verir.
def getVector(x1, y1, x2, y2):
    dX = x2 - x1
    dY = y2 - y1
    return (dX, dY)


# 9x9 luk alanda rastgele (x,y) koordinat degerleri uretip verir.
def createSeed(seedUzunlugu, startingPoint, droneCount):
    breakPoint = math.ceil(seedUzunlugu/droneCount)
    createdSeed = []
    pointArr = []
    pointArrTemp = []
    # Baslangic noktasini ekle.
    pointArrTemp.append(startingPoint)
    prevPoint = startingPoint
    for i in range(seedUzunlugu):
        # Alan disina cikmak yerine oldugu yerde kalmasi icin dongu degiskeni
        validDirection = True
        # 9x9 luk alan icerisinde yon bilgisi verene kadar rastgele yonler uret. Uygun yon geldiginde son koordinat bilgisini tut.
        while(validDirection):
            direction = random.randint(1,8)
            targetPoint = getDirectionToCoordinate(direction, prevPoint)
            if(isInTheField(targetPoint,9,9,0,0)):
                validDirection = False
                prevPoint = targetPoint
                # Gezilen alanlari diziye ekle.
                pointArrTemp.append(targetPoint)
                createdSeed.append(direction)
        if((i+1) % breakPoint == 0):
            pointArr.append(pointArrTemp)
        
    return createdSeed, pointArr


def getDirectionToCoordinate(direction, currentPos):
    if(direction == 1):
        point = (currentPos[0], currentPos[1] + 1)
    elif(direction == 2):
        point = (currentPos[0] - 1, currentPos[1] + 1)
    elif(direction == 3):
        point = (currentPos[0] - 1, currentPos[1])
    elif(direction == 4):
        point = (currentPos[0] - 1, currentPos[1] - 1)
    elif(direction == 5):
        point = (currentPos[0], currentPos[1] - 1)
    elif(direction == 6):
        point = (currentPos[0] + 1, currentPos[1] - 1)
    elif(direction == 7):
        point = (currentPos[0] + 1, currentPos[1])
    elif(direction == 8):
        point = (currentPos[0] + 1, currentPos[1] + 1)
    else:
        print("Unvalid direction")
        return None
    return point

            
# Verilen baslangic noktasi ve yon bilgisine gore koordinatlari dondurur.
def seedToCoordinate(directionSeed, startingPoint, droneCount):
    route = []
    breakPoint = math.ceil(len(directionSeed)/droneCount)
    for i in range(droneCount):
        routeTemp = []
        routeTemp.append(startingPoint)
        point = startingPoint
        for direction in range(breakPoint):
            fPoint = getDirectionToCoordinate(directionSeed[direction],point)
            if(isInTheField(fPoint,9,9,0,0)):
                point = fPoint
            routeTemp.append(point)
        route.append(routeTemp)
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
        if(marked.count(point)<1):
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
    lenCount = 0
    for i in range(2,len(route)):
        v1 = getVector(route[i-1][0],route[i-1][1], route[i][0], route[i][1])
        angle_ = getAngleBetweenVectors(v0,v1)
        if(angle_ is None):
            angle_ = 0
        else:
            #print("len Count : ", lenCount)
            lenCount += 1
            v0 = v1
        #print("Turning Angle ", i , " : ", angle_)
        angleRes += angle_
        #if(lenCount==0):
            #print("route : " , route)
        
    
    return angleRes / (lenCount)

# Fitness fonksiyonlari toplanarak genel fitness sonucu dondurulur.
def getFitnessScore(route, endPoint, droneCount):
    fitFinalDist = fitTurningAng = 0
    for i in range(droneCount):
        finalPoint = route[i][-1]
        fitFinalDist += getFinalDistancesFromEndPoint_Fitness(finalPoint, endPoint)
        fitTurningAng += getTurningAnglesInRoute_Fitness(route[i])
    
    finalRoute = []
    for j in range(droneCount):
        finalRoute += route[j]
    fitDiffPoint = getDifferentPointsCountInTheField_Fitness(finalRoute)
    #print("Diff p : ", fitDiffPoint)
    #print("Final Dist : ", fitFinalDist)
    #print("Turning and : ", fitTurningAng )
    
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
    
    #return parentX
    
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
        probablities.append(1/population[i].fitness) # fitness degeri az olanın ihtimali cok olmasi gerek.
    
    selection = random.choices(population, probablities,k=1)
    # Secilen degerin hangi indisde bulundugu bilgisi dondurulur.
    #print("Selected fitness : ", selection[0].fitness)
    return selection[0].idx


def applyMutationProbablity(kromozom, mutationProbablity,startingPoint):    
    prevPoint=startingPoint
    for i in range(1,len(kromozom)):
        prob = random.uniform(0.0, 1.0)
        #print(prob)
        j=0
        if(prob < mutationProbablity):
            while(j<i):
                targetPoint=getDirectionToCoordinate(kromozom[j],prevPoint)
                prevPoint=targetPoint
                j=j+1            
            validDirection=True
            #Mutasyon sonucu nokta alanın içindemi kontrolü
            direction= (random.randint(1,8) % 8)
            old_direction=kromozom[i]
            count=0
            while(validDirection and count<9):
                k=j      
                if(kromozom[i]!=direction and direction != 0 ):
                    kromozom[i]=direction
                    targetPoint1=getDirectionToCoordinate(kromozom[i],prevPoint)
                    prevPoint1=targetPoint1
                    k=k+1
                    while(k<len(kromozom) and isInTheField(prevPoint1,9,9,0,0)):
                        targetPoint1=getDirectionToCoordinate(kromozom[k],prevPoint1)
                        prevPoint1=targetPoint1
                        k=k+1
                    if(k>=len(kromozom)):
                        validDirection=False
                    else:
                        kromozom[i]=old_direction
                        direction=(direction+1) % 9
                else:
                    direction=(direction+1) % 9

                count=count+1
                #if(count == 9 ):
                #    print("mutasyon olmadı")
                

#Yolu çizdirme
def displayRoute(path):
    x=[]
    y=[]
    for point in path:
        x.append(point[0])
        y.append(point[1])   
    x1 = np.array(x)
    y1 = np.array(y)
    print("x : ",x1)
    print("y : ",y1)
    plt.xlim([-1,8])
    plt.ylim([-1,8])
    plt.plot(x1, y1)
    plt.show()


if __name__ == '__main__':
    #droneCount = input("Enter Drone Count : ")
    droneCount = 2
    populationCount = 1000
    mutationProbablity = 0.1
    startingPoint = endPoint = (0,0)
    population = []
    routes = []
    fitnessVals = []
    
    # Ilk populasyon olusturulur.
    for i in range(populationCount):
        pop,rout = createSeed(10, startingPoint, droneCount)
        #print("Directions : ", pop)
        #print("Routes : ", rout)
        population.append(pop)
        routes.append(rout)
        fitnessVals.append( FitnessIdx(i, getFitnessScore(routes[i], endPoint, droneCount)))
    
    #print("Fitness : ", fitnessVals[0].fitness)
    fitnessVals.sort(key=takeFitnessScore)
            
    # Yapilan siralamaya gore populasyondaki kromozomlarin secilme olasiliklarini atar.
    setPopulationProbablities(fitnessVals)
    
    endCondition = True
    generationCount = 1
    while endCondition:
        newPopulation = []
        newFitnessVals = []
        newRoutes = []
        for i in range(populationCount):
            newRoutesTemp = []
            parentX_Idx = randomSelection(fitnessVals)
            parentY_Idx = randomSelection(fitnessVals)
            
            parentX_kromozom = population[parentX_Idx]
            parentY_kromozom = population[parentY_Idx]
            
            # Fonksiyon icinde dizideki degerler degistiginden kopyasini gonderiyorum.
            child = applyCrossOver(parentX_kromozom.copy(), parentY_kromozom.copy())
            # Mutasyon ihtimalini ekler.
            applyMutationProbablity(child, mutationProbablity,(0,0))        
            
            newPopulation.append(child)
            rut = seedToCoordinate(child, startingPoint, droneCount)
            for j in range(droneCount):
                newRoutesTemp.append(rut[j])
                
            newRoutes.append(newRoutesTemp)
            newFitnessVals.append( FitnessIdx(i, getFitnessScore(newRoutes[i], endPoint, droneCount)))
            
        population = newPopulation
        routes = newRoutes
        fitnessVals = newFitnessVals
        fitnessVals.sort(key = takeFitnessScore)
        print("Fitness val : ", fitnessVals[0].fitness)
            
        if(fitnessVals[0].fitness < 0.18):
            endCondition = False
            print("Final fitness : ", fitnessVals[0].fitness)
            print("Final path : ", population[fitnessVals[0].idx])
            print("Generation Count : ", generationCount)
            path=seedToCoordinate( population[fitnessVals[0].idx],startingPoint, droneCount)
            displayRoute(path[0])

        generationCount += 1
    
        #endCondition = False
    #print("Parent X : ", parentX_kromozom)
    #print("Parent Y : ", parentY_kromozom)
    #print("Child : ", child)
    
    
    