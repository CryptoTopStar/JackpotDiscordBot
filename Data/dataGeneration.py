import math
import numpy as np
import datetime
from tqdm import tqdm
import csv

NUM_PEOPLE = 500
NUM_COMMUNITIES = 5

def generateData(min, mid, max, scale, numPeople):
    def binomial(mid, scale):
        return np.random.normal(loc=mid, scale=scale, size=None)

    myList = []
    for i in range(numPeople):
        myInt = -1
        while myInt < min or myInt > max:
            myInt = binomial(mid, scale)
        myList.append(myInt)
        
    for i, item in enumerate(myList):
        myList[i] = math.floor(item)
    
    return myList

def randomShuffle(list):
    np.random.shuffle(list)
    return list

def randomTime():
    start = 1640995200
    end = 1641182708
    myTime = np.random.randint(start, end)
    dt = datetime.datetime.fromtimestamp(myTime)
    return str(dt)

def saveData(data, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

NUM_DISCORD_MESSAGES = generateData(0, 15, 100, 3, NUM_PEOPLE)
NUM_DISCORD_REACTIONS = generateData(0, 20, 200, 5, NUM_PEOPLE)
NUM_OTHER_REACTIONS = generateData(0, 5, 50, 20, NUM_PEOPLE)
NUM_NEW_INTERACTIONS = generateData(0, 5, 20, 7, NUM_PEOPLE)
NUM_INVITES = generateData(0, 1, 10, 4, NUM_PEOPLE)
NUM_UN_INVITES = generateData(0, 0, 7, 1.25, NUM_PEOPLE)
NUM_VISITED_SERVER = randomShuffle(([0] * int(NUM_PEOPLE/4)) + ([1] * int(NUM_PEOPLE/4) * 3))
NUM_REPLIES = generateData(0, 3, 20, 12, NUM_PEOPLE)
NUM_FOLLOWERS = generateData(0, 2, 50, 25, NUM_PEOPLE)
NUM_FOLLOWING = generateData(0, 5, 75, 45, NUM_PEOPLE)
XP_FROM_RAIDS = generateData(0, 700, 6000, 2000, NUM_PEOPLE)
XP_FROM_QUESTS = generateData(0, 500, 10000, 2000, NUM_PEOPLE)

actionsByID = {1: NUM_DISCORD_MESSAGES, 2: NUM_DISCORD_REACTIONS, 3: NUM_OTHER_REACTIONS, 4: NUM_NEW_INTERACTIONS, 5: NUM_INVITES, -5: NUM_UN_INVITES, 9: NUM_VISITED_SERVER, 6: NUM_REPLIES, 8: NUM_FOLLOWERS, 7: NUM_FOLLOWING, 10: XP_FROM_RAIDS, 21: XP_FROM_QUESTS}
DATA = [["UNIQUE ID", "TASK TYPE", "XP OVERRIDE", "TIME", "COMMUNITY"]]

for person in tqdm(range(0, NUM_PEOPLE)):
    uniqueID = np.random.randint(100000000, 999999999)
    community = np.random.randint(0, NUM_COMMUNITIES)
    for action in actionsByID:
        if action in [1, 2, 3, 4, -5, 5, 9, 6, 7, 8]:
            for numTimes in range(0, actionsByID[action][person]):
                DATA.append([uniqueID, action, "NONE", randomTime(), community])
        elif action in [10, 21]:
            DATA.append([uniqueID, action, actionsByID[action][person], randomTime(), community])
            
saveData(DATA, "syntheticData.csv")