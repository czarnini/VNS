

import urllib.parse as prs
import requests
import ast

def generateDistanceMatrix(points):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

    units = "metric"
    destinations= parsePoints(points.values())
    origins = parsePoints(points.values())
    key = "AIzaSyBDG4CZIG5D3gpQz5WOCt5xHw60_vayWc8"
    myDistanceMatrix = list()

    query = base_url + prs.urlencode({'units':units,'origins':origins,'destinations':destinations,'key':key})

    parsedJSON = dict()
    with open(file="input.json", mode='r', encoding="utf-8") as inputFile:
        parsedJSON = ast.literal_eval(inputFile.read())
    for row in parsedJSON["rows"]:
        myDistanceMatrix.append(list())
        for element in row["elements"]:
            cost = ( 0 * element['distance']['value']/1000) + ( 1 * element['duration']['value'] )
            myDistanceMatrix[-1].append(cost)

    return myDistanceMatrix



def parsePoints(points):
    result = ""
    for tmp in points:
        tmp = tmp.strip()
        result += tmp +"|"
    return result[:-1]


def getRouteLink(points):
    base_url = "https://www.google.com/maps/dir/?"
    api = "1"
    origin = points[0]
    destination = points[-1]
    travelmode = "driving"
    waypoints = parsePoints(points[1:-1])
    return base_url + prs.urlencode({'api':api,'origin':origin,'destination':destination,'travelmode':travelmode,'waypoints':waypoints})
