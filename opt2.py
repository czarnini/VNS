import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math


def countDist(a, b):
    return math.sqrt( (math.pow(a[0]-b[0],2)) + (math.pow(a[1]-b[1],2)) )

def createGraph(perKeys):
    global points
    global costBefore

    G = nx.DiGraph()
    for i in  range (0, len(perKeys) - 1):
        G.add_edge(perKeys[i], perKeys[i+1])
        costBefore += countDist(points[perKeys[i]], points[perKeys[i+1]])
    plt.figure(3,figsize=(20,20))
    nx.draw(G, points)
    plt.savefig("graph_before.png")
    plt.clf()
    return G

def opt2(points):
    isBroken = False
    for i in range (0, len(perKeys) - 2):
        b = points[perKeys[i]]
        c = points[perKeys[i+1]]
        for j in range (i+2, len(points) -1 ):
            # print(G.edges())
            e = points[perKeys[j]]
            f = points[perKeys[j+1]]
            if countDist(b,c) + countDist(e,f) > countDist(b,e) + countDist(c,f):
                perKeys[i+1], perKeys[j] = perKeys[j],  perKeys[i+1]

                isBroken = True
                break

    return isBroken


def generateTour():
    global perKeys
    perKeys = list( np.random.permutation(list(points.keys())))
    tmp = perKeys.index(1)
    perKeys[0], perKeys[tmp] = perKeys[tmp], perKeys[0]
    return perKeys



def countDistanceBetweenTours(tourA, tourB):




points = { 1 :(565.0, 575.0), 2 :(25.0, 185.0), 3 :(345.0, 750.0), 4 :(945.0, 685.0),
5 :(845.0, 655.0), 6 :(880.0, 660.0), 7 :(25.0, 230.0), 8 :(525.0, 1000.0),
9 :(580.0, 1175.0), 10:( 650.0, 1130.0), 11:( 1605.0, 620.0), 12:( 1220.0, 580.0),
13:( 1465.0, 200.0), 14:( 1530.0, 5.0), 15:( 845.0, 680.0), 16:( 725.0, 370.0),
17:( 145.0, 665.0), 18:( 415.0, 635.0), 19:( 510.0, 875.0), 20:( 560.0, 365.0),
21:( 300.0, 465.0), 22:( 520.0, 585.0), 23:( 480.0, 415.0), 24:( 835.0, 625.0),
25:( 975.0, 580.0), 26:( 1215.0, 245.0), 27:( 1320.0, 315.0), 28:( 1250.0, 400.0),
29:( 660.0, 180.0), 30:( 410.0, 250.0), 31:( 420.0, 555.0), 32:( 575.0, 665.0),
33:( 1150.0, 1160.0), 34:( 700.0, 580.0), 35:( 685.0, 595.0), 36:( 685.0, 610.0),
37:( 770.0, 610.0), 38:( 795.0, 645.0), 39:( 720.0, 635.0), 40:( 760.0, 650.0),
41:( 475.0, 960.0), 42:( 95.0, 260.0), 43:( 875.0, 920.0), 44:( 700.0, 500.0),
45:( 555.0, 815.0), 46:( 830.0, 485.0), 47:( 1170.0, 65.0), 48:( 830.0, 610.0),
49:( 605.0, 625.0), 50:( 595.0, 360.0), 51:( 1340.0, 725.0), 52:( 1740.0, 245.0)}

perKeys = list()
currLowest = 1000000
kMax = 10;


while True:
    costBefore = 0
    createGraph(points)

    perKeys = list( np.random.permutation(list(points.keys())))
    tmp = perKeys.index(1)
    perKeys[0], perKeys[tmp] = perKeys[tmp], perKeys[0]





    a=0
    while opt2(points) and a < 1500:
        a += 1

    G = nx.DiGraph()
    costAfter = 0
    for i in  range (0, len(perKeys) - 1):
        G.add_edge(perKeys[i], perKeys[i+1])
        costAfter += countDist(points[perKeys[i]], points[perKeys[i+1]])
    if costAfter < currLowest:
        print("Found Better solution:", costAfter, "Progress:", (currLowest - costAfter)*100/currLowest, "%")
        currLowest = costAfter
        plt.figure(3,figsize=(12,12))
        nx.draw(G, points)
        plt.savefig("graph_after.png")
