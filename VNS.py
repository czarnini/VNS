import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import random

import FunWithAPI


class VNS_OPT:
    def generateGraph(self):
        G = nx.DiGraph()
        cost = 0
        for i in  range (0, len(self.perKeys) - 1):
            G.add_edge(self.perKeys[i], self.perKeys[i+1])
            cost += self.countDist(self.perKeys[i], self.perKeys[i+1])
        G.add_edge(self.perKeys[-1], self.perKeys[0])
        self.tmpCost = cost
        return G

    def drawGraph(self, G ,fileName):
        plt.figure(3, figsize=(40,40))
        nx.draw(G, self.points)
        plt.savefig(fileName)
        plt.clf()
        return

    def opt2(self):
        # for i in range (0, 20*len(self.perKeys)):
        stopIndex = 0
        while True and stopIndex < 10000:
            stopIndex+=1
            # print(i)
            tmp = 0
            isBroken = False
            for i in range (0, len(self.perKeys) - 2):
                for j in range (i+2, len(self.perKeys) -1 ):
                    A = self.countDist(self.perKeys[i],self.perKeys[i+1]) + self.countDist(self.perKeys[j],self.perKeys[j+1])
                    B = self.countDist(self.perKeys[i],self.perKeys[j]) + self.countDist(self.perKeys[i+1],self.perKeys[j+1])
                    if  A>B:
                        tmp += A - B
                        self.swap(i+1, j)
                        isBroken = True
                        break
            # if not isBroken:
            #     if self.countDist(self.perKeys[i],self.perKeys[i+1]) + self.countDist(self.perKeys[-2],self.perKeys[-1]) > self.countDist(self.perKeys[i],self.perKeys[-2]) + self.countDist(self.perKeys[i+1],self.perKeys[-1]):
            #         self.swap(i+1, len(self.perKeys)-1))
            if tmp < 10:
                break
    def swap(self, i, j):
        prefix = self.perKeys[0:i]
        toSwap = self.perKeys[i:j+1]
        sufix = self.perKeys[j+1:]
        for index in range(1, len(toSwap)):
            toSwap[index-1], toSwap[-index] = toSwap[-index],  toSwap[index-1]
        self.perKeys = prefix + toSwap + sufix



    def countDist(self, a, b):
        return self.matrix[a][b]

    def generateTour(self):
        self.perKeys = list( np.random.permutation(list(self.points.keys())))


    def generateNeighbourTrip(self, k, base):

        dontMoveIndexes = list()
        dontMoveValues = list()
        i = 0
        while i < k:
            candidate = int ( len(base) * random.random() ) -1
            if not candidate in dontMoveIndexes:
                dontMoveIndexes.append(candidate)
                dontMoveValues.append( (base[candidate], base[candidate+1]))
                i += 1

        result = list(np.random.permutation(base))
        for j in range (0, len(dontMoveValues)):
            tmpIndex1 = result.index(dontMoveValues[j][0])
            tmpIndex2 = result.index(dontMoveValues[j][1])
            result[dontMoveIndexes[j]]    , result[tmpIndex1] = result[tmpIndex1], result[dontMoveIndexes[j]]
            result[dontMoveIndexes[j] +1 ], result[tmpIndex2] = result[tmpIndex2], result[dontMoveIndexes[j]+1]
        self.perKeys = result


    def initialize(self):
        self.readAddressFile()
        self.readTimeFile()
        self.matrix = FunWithAPI.generateDistanceMatrix(self.points )
        self.K_MAX = len(self.points)
        self.generateTour();
        self.opt2()
        self.x = self.perKeys
        self.generateGraph()
        self.currentBest = self.tmpCost
        return


    def readAddressFile(self):
        with open("adresy.txt", encoding="utf8") as file:
            lines = file.readlines()
        lineIndex = 0
        for line in lines:
            self.points[lineIndex] = line
            lineIndex += 1

    def readTimeFile(self):
        with open("time.txt", encoding="utf8") as file:
            lines = file.readlines()
        for line in lines:
            self.time.append(list(map(int,line.split())))
        print(self.time)

    def optimize(self):
        while True:
            k = self.K_MAX - 1
            while k > 0:
                self.generateNeighbourTrip(k, self.x)
                self.opt2()
                G = self.generateGraph()
                if self.tmpCost < self.currentBest and True:
                    print ("New best Found", self.currentBest,"\t",self.tmpCost,"\t",self.perKeys)
                    self.currentBest = self.tmpCost
                    self.x = self.perKeys
                    k = self.K_MAX - 1
                else:
                    k -= 1
        return

    def getBestSolution(self):
        bestSolution = list()
        for tmp in self.x:
            bestSolution.append(self.points[tmp])
        return bestSolution

    def isFeasible(self):
        tmpCost = 0
        for i  in range (1, len(self.perKeys)):
            tmpCost += self.countDist(self.perKeys[i-1],self.perKeys[i])
            if( tmpCost > self.time[self.perKeys[i]][1]): #  + tmpCost < self.time[tmp][0] or ??
                return False
        return True

    avgDist = int()
    points = dict()
    K_MAX = int()
    x = list()
    perKeys = list()
    currentBest = 9999999
    matrix = list()
    time = list()

try:
    optimizer = VNS_OPT()
    optimizer.initialize()
    optimizer.optimize()
except KeyboardInterrupt:
    # print(FunWithAPI.getRouteLink(optimizer.getBestSolution()),"\n\n\n", optimizer.currentBest)
    tmpCost = 0
    for i  in range (1, len(optimizer.x)):
        print (optimizer.x[i-1] +1, optimizer.points[optimizer.x[i-1]].strip('\n'),'\t' , tmpCost)
        tmpCost += optimizer.countDist(optimizer.x[i-1],optimizer.x[i])
    print(optimizer.x[-1]+1,optimizer.points[optimizer.x[-1]].strip('\n'), '\t' ,tmpCost)
