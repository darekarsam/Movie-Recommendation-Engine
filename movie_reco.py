# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 02:05:38 2016

@author: Sameer
@title  : Movie Recommendation System using Movielens Dataset
"""

import numpy as np
from scipy.spatial import distance
import math

# get the wieghted average for the rating so calculate the similarity between 2 vectors, 1 is exactly similar and 0 means dissimilar
def getDistanceMatrix(matrix,dMatrix):
    i=0   
    for i in range(1,len(matrix)-1):
        if(i%100==0):
            print "Calculated matrix for first " + str(i)+" values" 
        for j in range(i+1,len(matrix)):
            if max(matrix[i])==0 or max(matrix[j])==0: #either of the vector is empty
                dMatrix[i][j]=dMatrix[j][i]=-1
            else:
                if(i!=j):
                    dMatrix[i][j]=dMatrix[j][i]=(1.0/distance.euclidean(matrix[i],matrix[j])) #similarity=1/distance
                    #dMatrix[i][j]=dMatrix[j][i]=(1.0/distance.cityblock(matrix[i],matrix[j]))  #manhattan Distance
                    #dMatrix[i][j]=dMatrix[j][i]=(1.0/distance.chebyshev(matrix[i],matrix[j]))  #Lmax Distance
    return


#generating k nearest neighbours for a user who has seen the movie which the user has not seen
def getNNeighbours(matrix,dMatrix,user,movie):
    nearestNeighbours=[]
    distUser=[]
    noMovieData=[]
    k=10 #considering k=10
    similarityCount=0
#get the distance betwwen 2 vectors and sort to get the most closer ones
    for i in range(1,len(dMatrix)):
        if matrix[i][movie]!=0:            
            distUser.insert(i,[matrix[i][movie],dMatrix[i][user]]) ##[rating][distance]
            similarityCount +=1
    if similarityCount==0:
        # couldn't Find similar user who watched the Movie
        noMovieData.insert(i,[user,movie])
    nearestNeighbours=sorted(distUser, key=lambda x: x[1],reverse=True)
    return nearestNeighbours[0:k]

def getWeightedAvg(lista):
    avg=0.0
    suma=0.0
    sumw=0
    for i in range(0,len(lista)):
        #suma=suma+lista[i][0]
        #sumw=sumw+1
        suma=suma+lista[i][0]*lista[i][1]
        sumw=sumw+lista[i][1]
    if(sumw==0):
        return -1
    avg=suma/sumw
    return float(avg)

def getRecomendation(matrix,dMatrix,user,movie):
    reco=-1
    neighbours=[]
    neighbours=getNNeighbours(matrix,dMatrix,user,movie)
    if len(neighbours)>0:
        reco=getWeightedAvg(neighbours)
    return reco

def buildRecommendationMatrix(matrix,dMatrix):
    recoMatrix=[[0 for x in range(1683)] for y in range(944)]
    reco=0
    for user in range(1,944):
        for movie in range(1,1683):
            if matrix[user][movie]==0:
                reco=getRecomendation(matrix,dMatrix,user,movie)#get n neighbours for a movie
                recoMatrix[user][movie]=reco
    return recoMatrix

#Function to calculate Mean Absolute Difference
def calcMAD(recoMatrix,testMatrix):
    madist=0L
    rij=sumrij=0L
    pij=0L
    tij=summation=0L
    temp=0L
    for i in range(944):
        for j in range(1683):
            if testMatrix[i][j]==0:
                rij=0
            else:
                rij=1
            pij=recoMatrix[i][j]
            tij=testMatrix[i][j]
            sumrij=sumrij+rij
            temp=math.fabs(rij*(pij-tij))
            summation=summation+temp
    madist=(1.0/sumrij)
    madist=madist*summation
    return madist

#Main thread
dataset=[]
print "Execution Started"
movieUserRatingMatrix=[[0 for x in range(1683)] for x in range(944)] #creating matrix of 0 for no of user*no of movies
distanceEMatrix =[[0 for x in range(944)] for x in range(944)]
manhattanDMatrix=[[0 for x in range(944)] for x in range(944)]
LmaxDMatrix=[[0 for x in range(944)] for x in range(944)]
x=y=rating=0
distanceMatrix=distanceEMatrix
dm=0
madAll=[]
f=open("--enter the path--\\u1.base",'r')
for line in f:
    x=int(line.split('\t')[0])
    y=int(line.split('\t')[1])
    rating=int(line.split('\t')[2])
    timestamp=int(line.split('\t')[3].strip())
    dataset.append([x,y,rating])
    movieUserRatingMatrix [x][y]=rating  #creating matrix
f.close()
f = open("--enter the path--\\movieUserMatrix", "w")
f.write("\n".join(map(lambda x: str(x), movieUserRatingMatrix)))
f.close()
print "Distance Matrix calculation Started"
#distanceMatrix=
getDistanceMatrix(movieUserRatingMatrix,distanceMatrix)
f = open("--enter the path here--\\EdistanceMatrix", "w")
f.write("\n".join(map(lambda x: str(x), distanceMatrix)))
f.close()
print "Distance Matrix calculated"
print "Building Recommendation Matrix"
recoMatrix=buildRecommendationMatrix(movieUserRatingMatrix,distanceMatrix)
f = open("--enter the path here--\\recoMatrix", "w")
f.write("\n".join(map(lambda x: str(x), recoMatrix)))
f.close()
print"Recomendation Matrix calculated"
testDataset=[]
testUserRatingMatrix=[[0 for a in range(1683)] for b in range(944)] 
f=open("--enter the path here--\\u1.test",'r')
for line in f:
    x=int(line.split('\t')[0])
    y=int(line.split('\t')[1])
    rating=int(line.split('\t')[2])
    timestamp=int(line.split('\t')[3].strip())
    testDataset.append([x,y,rating])
    testUserRatingMatrix[x][y]=rating  #creating matrix
print "testUsermatrix generated"
f.close()
f = open("--enter the path here--\\testMatrix", "w")
f.write("\n".join(map(lambda x: str(x), testUserRatingMatrix)))
f.close()

#calculating Mean Absolute Distance(MAD)
mad=calcMAD(recoMatrix,testUserRatingMatrix)
print "The Mean Absolute Difference is : "+str(mad)


"""
#for file u1.base and u1.test

Output-- for euclidean distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.876882216708

Output-- for Manhattan distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.855087844742

Output-- for Lmax distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.848988612416

#for file u2.base and u2.test
Output-- for euclidean distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.874923419154


Output-- for Manhattan distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.847523623145

Output-- for Lmax distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.855261631281

#for file u3.base and u3.test
Output-- for euclidean distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.863880102326    


Output-- for Manhattan distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.842032014474


Output-- for Lmax distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.8553756693

#for file u4.base and u4.test
Output-- for euclidean distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.863929778663  


Output-- for Manhattan distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.843994582053


Output-- for Lmax distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.848122196315

#for file u5.base and u5.test
Output-- for euclidean distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.864636243817


Output-- for Manhattan distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.846763559806


Output-- for Lmax distance
Execution Started
Distance Matrix calculation Started
Calculated matrix for first 100 values
Calculated matrix for first 200 values
Calculated matrix for first 300 values
Calculated matrix for first 400 values
Calculated matrix for first 500 values
Calculated matrix for first 600 values
Calculated matrix for first 700 values
Calculated matrix for first 800 values
Calculated matrix for first 900 values
Distance Matrix calculated
Building Recommendation Matrix
Recomendation Matrix calculated
testUsermatrix generated
The Mean Absolute Difference is : 0.857640404513


"""
