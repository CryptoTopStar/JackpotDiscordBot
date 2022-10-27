import csv

DEFAULT_WEIGHT = 1
INDIVIDUAL_WEIGHT = {}
COMMUNITY_WEIGHT = {}
XP_AWARDS = {1:40, 2:15, 3:200, 4:800, 5:700, -5:-700, 6:500, 7:1000, 8:400, 9:150, 10:600, 11:200, 12:400, 13:0, 14:1000, 15:2000, 16:3000, 17:3500, 18:3600, 19:4000, 20:5000, 21:0}

## DATA SCHEMA
## UNIQUE ID | TASK TYPE | XP OVERRIDE | TIME | COMMUNITY
def readCSV(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

## Create a class to represent a user and number of interactions
class User:
    def __init__(self, id, community):
        self.id = id
        self.community = community
        self.xpOverride = 0
        self.counter = {1:0, 2:0, 3:0, 4:0, 5:0, -5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0}
        self.counterOverride = {1:0, 2:0, 3:0, 4:0, 5:0, -5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0}
        self.finalXP = None

## Uses XP Values to calculate XP, ignores XP Override
def calXP(individual):
    xp = 0
    for key, value in individual.counter.items():
        xp += value * XP_AWARDS[key]
    return xp

## Function to update User object
def updateCounter(individual, point):
    if point[2] != "NONE":
        individual.xpOverride += int(point[2])
        individual.counterOverride[int(point[1])] += 1
    else:
        individual.counter[int(point[1])] += 1
        
## Function to save CSV
def saveData(data, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

rawData = readCSV("syntheticData.csv")
roaster = {}

for point in rawData[1:]:
    unqiueID = str(point[0]) + "===" + str(point[4])
    if unqiueID not in roaster:
        individual = User(point[0], point[4])
        roaster[unqiueID] = individual
    else:
        individual = roaster[unqiueID]
    
    updateCounter(individual, point)

listXP = [["ID", "Community", "XP"]]
for keys in roaster:
    weight = DEFAULT_WEIGHT
    id = keys.split("===")[0]
    community = keys.split("===")[1]
    
    if id in INDIVIDUAL_WEIGHT:
        weight *= INDIVIDUAL_WEIGHT[id]
    if community in COMMUNITY_WEIGHT:
        weight *= COMMUNITY_WEIGHT[community]
        
    xp = weight * (calXP(roaster[keys]) + roaster[keys].xpOverride)
    roaster[keys].finalXP = xp
    listXP += [[id, community, xp]]
    
saveData(listXP, "XP_data.csv")
    