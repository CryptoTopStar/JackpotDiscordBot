import csv
from datetime import datetime
import pandas as pd
import math

DEFAULT_WEIGHT = 1
INDIVIDUAL_WEIGHT = {}
COMMUNITY_WEIGHT = {}
XP_AWARDS = {1:40, 2:15, 3:200, 4:800, 5:700, -5:-700, 6:500, 7:1000, 8:400, 9:150, 10:600, 11:200, 12:400, 13:0, 14:1000, 15:2000, 16:3000, 17:3500, 18:3600, 19:4000, 20:5000, 21:0}

##TIME = datetime.datetime.now().strftime("%m/%d/%y %H:%M")
TIME = datetime.strptime("1/2/22 20:05", "%m/%d/%y %H:%M")

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
    def __init__(self, name, unqiueIdentifier, id, community, url, handle = None, wallet = None):
        self.name = name
        self.full = unqiueIdentifier
        self.id = id
        self.handle = handle
        self.wallet = wallet
        self.community = community
        self.pfp = url
        self.referal = None
        self.joinTime = datetime.now().strftime("%m/%d/%y %H:%M")
        self.lastActive = datetime.now().strftime("%m/%d/%y %H:%M")
        self.xpOverride = 0
        self.counter = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, -5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0}
        self.counterOverride = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, -5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0}
        self.finalXP = None
        
    def getReferal(self):
        return self.referal
    
    def updateInfo(self, handle, wallet):
        if handle != None and handle != "":
            self.handle = handle
        if wallet != None and wallet != "":
            self.wallet = wallet
    
    def reprJSON(self):
        return dict(name = self.name, full = self.full, id = self.id, handle = self.handle, wallet = self.wallet, community = self.community, pfp = self.pfp, referal = self.referal, joinTime = self.joinTime, lastActive = self.lastActive, xpOverride = self.xpOverride, counter = self.counter, counterOverride = self.counterOverride, finalXP = self.finalXP)
                    
class TwitterRaid:
    def __init__(self, title, url, boosted, retweet, react, comment):
        self.title = title
        self.link = url
        self.boosted = boosted
        self.retweet = retweet
        self.react = react
        self.comment = comment
        self.date = datetime.now().strftime("%m/%d/%y %H:%M")
        self.completed = {}
        
    def reprJSON(self):
        return dict(title = self.title, link = self.link, boosted = self.boosted, retweet = self.retweet, react = self.react, comment = self.comment, date = self.date, completed = self.completed)
    
class Mission:
    def __init__(self, title, description, xp, supply = None, perPerson = None):
        if supply != None:
            self.limit = supply
        else:
            self.limit = math.inf
        
        if perPerson != None:
            self.personLimit = perPerson
        else:
            self.personLimit = math.inf
            
        self.title = title
        self.description = description
        self.date = datetime.now().strftime("%m/%d/%y %H:%M")
        self.xp = xp
        self.count = 0
        self.numPeople = 0
        self.completed = {}
        
    def reprJSON(self):
        return dict(title = self.title, description = self.description, date = self.date, xp = self.xp, count = self.count, numPeople = self.numPeople, completed = self.completed, limit = self.limit, personLimit = self.personLimit)

class Server:
    def __init__(self, name, id, url):
        self.name = name
        self.id = id
        self.pfp = url
        self.joinTime = datetime.now().strftime("%m/%d/%y %H:%M")
        self.leaderboard = serverLeaderboard()
        self.maxMembers = 50
    
    def reprJSON(self):
        return dict(name = self.name, id = self.id, pfp = self.pfp, joinTime = self.joinTime, leaderboard = self.leaderboard.reprJSON(), maxMembers = self.maxMembers)

class globalLeaderboard:
    def __init__(self):
        self.leaderboard = pd.DataFrame(columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges"])
    
    def update(self, memberID, XP, serverID):
        if memberID in self.leaderboard["memberID"]:
            if serverID in self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "servers"]:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "servers"][serverID] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "servers"][serverID]
            else:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "servers"][serverID] = XP
        else:
            ##self.leaderboard = self.leaderboard.append({"memberID":memberID, "memberXP":XP, "memberRank":None, "trend":0, "servers":{serverID:XP}, "badges":None}, ignore_index = True)
            self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame([[memberID, XP, None, 0, {serverID:XP}, None]], columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges"])], ignore_index = True)
        self.leaderboard = self.leaderboard.sort_values(by = ["memberXP"], ascending = False)
        
        def trend(old, new):
            if old > new:
                return 1, new
            if old < new:
                return -1, new
            if old == new:
                return 0, new
        
        for i in range(len(self.leaderboard)):
            oldRank = self.leaderboard.loc[i, "memberRank"]
            if oldRank == None:
                oldRank = 1 
            if i == 0:
                newTrend, newRank = trend(oldRank, 1)
            else:
                if self.leaderboard.loc[i, "memberXP"] == self.leaderboard.loc[i-1, "memberXP"]:
                    newTrend, newRank = trend(oldRank, self.leaderboard.loc[i-1, "memberRank"])
                else:
                    newTrend, newRank = trend(oldRank, i+1)
                   
            self.leaderboard.loc[i, "memberRank"] = newRank
            self.leaderboard.loc[i, "trend"] = newTrend
            
    def search(self, string):
        return self.leaderboard[self.leaderboard["memberID"].str.contains(string)]
    
    def getRankTrendXP(self, memberID):
        row = self.leaderboard[self.leaderboard["memberID"] == memberID]
        rank = row["memberRank"].values[0]
        trend = row["trend"].values[0]
        XP = row["memberXP"].values[0]
        return rank, trend, XP
    
    def reprJSON(self):
        return self.leaderboard.to_dict(orient = "records")
        
        
class serverLeaderboard:
    def __init__(self):
        ## init an empty pandas dataframe with the following columns:
        ## memberID, memberXP, memberRank, trend
        self.leaderboard = pd.DataFrame(columns = ["memberID", "memberXP", "memberRank", "trend"])
    
    def update(self, memberID, XP):
        if memberID in self.leaderboard["memberID"]:
            self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
        else:
            #self.leaderboard = self.leaderboard.append({"memberID":memberID, "memberXP":XP, "memberRank":None, "trend":0}, ignore_index = True)
            self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame({"memberID":[memberID], "memberXP":[XP], "memberRank":[None], "trend":[0]})], ignore_index = True)
            
        self.leaderboard = self.leaderboard.sort_values(by = ["memberXP"], ascending = False)
        ## assign new ranks based on new XP, if XP is the same, keep the same rank
        ## if old rank is greater than new rank, trend = 1
        ## if old rank is less than new rank, trend = -1
        ## if old rank is the same as new rank, trend = 0
        
        def trend(old, new):
            if old > new:
                return 1, new
            if old < new:
                return -1, new
            if old == new:
                return 0, new
            
        for i in range(len(self.leaderboard)):
            oldRank = self.leaderboard.loc[i, "memberRank"]
            if oldRank == None:
                oldRank = 1 
            if i == 0:
                newTrend, newRank = trend(oldRank, 1)
            else:
                if self.leaderboard.loc[i, "memberXP"] == self.leaderboard.loc[i-1, "memberXP"]:
                    newTrend, newRank = trend(oldRank, self.leaderboard.loc[i-1, "memberRank"])
                else:
                    newTrend, newRank = trend(oldRank, i+1)
                   
            self.leaderboard.loc[i, "memberRank"] = newRank
            self.leaderboard.loc[i, "trend"] = newTrend
            
    def search(self, string):
        ## search all member IDs for string, returning all values of the leaderboard for match
        ## for example, the string "ABC" would return all rows with memberID containing "ABC"
        return self.leaderboard[self.leaderboard["memberID"].str.contains(string)]
    
    def reprJSON(self):
        return self.leaderboard.to_dict(orient = "records")
    
    def getRankTrendXP(self, memberID):
        row = self.leaderboard[self.leaderboard["memberID"] == memberID]
        rank = row["memberRank"].values[0]
        trend = row["trend"].values[0]
        XP = row["memberXP"].values[0]
        return rank, trend, XP

"""
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

## iterate through all data points
for point in rawData[1:]:
    taskTime = datetime.strptime(point[3], "%m/%d/%y %H:%M")
    ## if taskTime is more than 48 hours before TIME, ignore
    if (TIME - taskTime).days > 2:
        continue
    
    unqiueID = str(point[0]) + "===" + str(point[4])
    if unqiueID not in roaster:
        individual = User(point[0], point[4])
        roaster[unqiueID] = individual
    else:
        individual = roaster[unqiueID]
    
    updateCounter(individual, point)

## calculate finalXP and organize data into a list of lists
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
    """