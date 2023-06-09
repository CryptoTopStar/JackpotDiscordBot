import csv
from datetime import datetime
import pandas as pd
import math
import api as api

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

class Member:
    def __init__(self, name, id, communityID):
        self.name = name
        self.id = id
        self.communityID = communityID
        self.date = datetime.now().strftime("%m/%d/%y %H:%M")
        self.interactions = []
        self.referer = None
    
    def reprJSON(self):
        return dict(name=self.name, id=self.id, communityID=self.communityID, new=self.new)
    
class userBadge:
    def __init__(self, userID):
        self.userID = userID
        self.badges = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "M1": [], "M2": [], "M3": [], "M4": [], "M5": [], "M6": [], "M7": [], "M8": []}
    
    def storeBadge(self, badge, serverID = "GLOBAL"):
        if serverID not in self.badges[str(badge)]:
            self.badges[str(badge)].append(serverID)
        else:
            return False
        
        if len(self.badges[str(badge)]) == 1:
            return True
        
        return False
    
    def deleteBadge(self, badge, serverID = "GLOBAL"):
        try:
            self.badges[str(badge)].remove(serverID)
        except:
            pass
        
        if len(self.badges[str(badge)]) == 0:
            return True
        
        return False

## Create a class to represent a user and number of interactions
class User:
    def __init__(self, name, unqiueIdentifier, id, community, url, twitterOBJ = None, wallet = None):
        ## twitterOBJ = [access_token, access_token_secret, user_id, screen_name]
        if twitterOBJ == None:
            twitterOBJ = [None, None, None, None]
        else:
            twitterOBJ = twitterOBJ[:3] + ["@" + str(twitterOBJ[3])]
        self.name = name
        self.full = unqiueIdentifier
        self.id = id
        self.twitterOBJ = twitterOBJ[:3]
        self.handle = twitterOBJ[3]
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
        return dict(name = self.name, full = self.full, id = self.id, handle = self.handle, wallet = self.wallet, access_token = self.twitterOBJ[0], access_token_secret = self.twitterOBJ[1], user_id = self.twitterOBJ[2], community = self.community, pfp = self.pfp, referal = self.referal, joinTime = self.joinTime, lastActive = self.lastActive, xpOverride = self.xpOverride, counter = self.counter, counterOverride = self.counterOverride, finalXP = self.finalXP)
                    
class TwitterRaid:
    def __init__(self, title, url, boosted, retweet, react, comment):
        self.title = title
        self.link = url
        self.id = int(url.split("/")[-1].split("?")[0])
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
            self.limit = int(supply)
        else:
            self.limit = math.inf
        
        if perPerson != None:
            self.personLimit = int(perPerson)
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

class ServerPickle:
    def __init__(self, SERVER):
        self.name = str(SERVER.name)
        self.id = str(SERVER.id)
        print(SERVER.pfp)
        self.pfp = SERVER.pfp
        self.joinTime = str(SERVER.joinTime)
        print(SERVER.maxMembers)
        self.maxMembers = SERVER.maxMembers
        self.optInCount = SERVER.optInCount
        print(SERVER.invites)
        self.invites = SERVER.invites
        print(SERVER.newMembers)
        self.newMembers = SERVER.newMembers
        self.endDate = SERVER.endDate
        print(SERVER.endMessage)
        self.endMessage = SERVER.endMessage
        ##self.twitterOBJ = SERVER.twitterOBJ
        ##self.handle = SERVER.handle
        ##self.numWins = SERVER.numWins
        ##self.channelNames = SERVER.channelNames


class Server:
    def __init__(self, name, id, url, invites):
        self.name = name
        self.id = id
        self.pfp = url
        self.joinTime = datetime.now().strftime("%m/%d/%y %H:%M")
        self.leaderboard = serverLeaderboard(id)
        self.persistantLeaderboard = serverLeaderboard(None)
        self.maxMembers = 50
        self.optInCount = 0
        self.invites = invites
        self.welcomeMessages = [None, None] ## [get-started, user-settings]
        self.joinNow = None
        self.newMembers = {} ## {memberID: MemberOBJ, ... }
        self.endDate = None
        self.endMessage = None
        self.twitterOBJ = None
        self.handle = None
        self.numWins = 0
        self.channelNames = {"get-started" : "💰｜get-started", "user-settings" : "💰｜user-settings", "leaderboard" : "💰｜leaderboard", "raids" : "💰｜raids", "quests" : "💰｜quests", "add-quests" : "💎｜add-quests", "mission-approval" : "💎｜mission-approval", "launch-raid" : "💎｜launch-raid", "notifs" : "💰｜notifs"}
    
    def clear(self):
        self.leaderboard = serverLeaderboard()
    
    def reprJSON(self):
        return dict(name = self.name, id = self.id, pfp = self.pfp, joinTime = self.joinTime, leaderboard = self.leaderboard.reprJSON(), maxMembers = self.maxMembers)

class globalLeaderboard:
    def __init__(self):
        self.leaderboard = pd.DataFrame(columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges", "questXP", "raidXP"])
    
    def update(self, memberID, XP, serverID, quest = False, raid = False):
        ## store the memberID of the top 25% of the leaderboard, round up
        try:
            oldTop25 = self.leaderboard["memberID"].iloc[:math.ceil(len(self.leaderboard) * 0.25)]
            oldTopQuest = self.leaderboard.loc[self.leaderboard["questXP"] == self.leaderboard["questXP"].max(), "memberID"]
            oldTopRaid = self.leaderboard.loc[self.leaderboard["raidXP"] == self.leaderboard["raidXP"].max(), "memberID"]
        except:
            oldTop25, oldTopQuest, oldTopRaid = [], [], []
            
        ## store the memberID of the top 5% of the leaderboard, round up
        try:
            oldTop5 = self.leaderboard["memberID"].iloc[:math.ceil(len(self.leaderboard) * 0.05)]
        except:
            oldTop5 = []
            
        try:
            oldTopEarner = self.leaderboard["memberID"].iloc[0]
        except:
            oldTopEarner = None
        
        if memberID in list(self.leaderboard["memberID"]):
            if serverID in self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "servers"]:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["servers"][0][serverID] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["servers"][0][serverID]
            else:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["servers"][0][serverID] = XP
                
            if quest:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "questXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "questXP"]
            elif raid:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "raidXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "raidXP"]
        else:
            if quest:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame([[memberID, XP, None, 0, {serverID:XP}, None, XP, 0]], columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges", "questXP", "raidXP"])], ignore_index = True)
            elif raid:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame([[memberID, XP, None, 0, {serverID:XP}, None, 0, XP]], columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges", "questXP", "raidXP"])], ignore_index = True)
            else:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame([[memberID, XP, None, 0, {serverID:XP}, None]], columns = ["memberID", "memberXP", "memberRank", "trend", "servers", "badges"])], ignore_index = True)
        
        self.leaderboard = self.leaderboard.sort_values(by = ["memberXP"], ascending = False)
        self.leaderboard = self.leaderboard.reset_index(drop = True)
        
        try:
            newTop25 = self.leaderboard["memberID"].iloc[:math.ceil(len(self.leaderboard) * 0.25)]
            newTopQuest = self.leaderboard.loc[self.leaderboard["questXP"] == self.leaderboard["questXP"].max(), "memberID"]
            newTopRaid = self.leaderboard.loc[self.leaderboard["raidXP"] == self.leaderboard["raidXP"].max(), "memberID"]
        except:
            newTop25, newTopQuest, newTopRaid = [], [], []
            
        try:
            newTop5 = self.leaderboard["memberID"].iloc[:math.ceil(len(self.leaderboard) * 0.05)]
        except:
            newTop5 = []
            
        try:
            newTopEarner = self.leaderboard["memberID"].iloc[0]
        except:
            newTopEarner = None
            
        ## find any new members in the top 25% of the leaderboard and find members who have fallen out of the top 25%
        newMembers25 = list(set(newTop25) - set(oldTop25))
        fallenMembers25 = list(set(oldTop25) - set(newTop25))
        api.ribbon1(newMembers25, fallenMembers25)
        
        ## find any new members in the top 5% of the leaderboard and find members who have fallen out of the top 5%
        newMembers5 = list(set(newTop5) - set(oldTop5))
        fallenMembers5 = list(set(oldTop5) - set(newTop5))
        api.ribbon2(newMembers5, fallenMembers5)
        
        newMembersRaid = list(set(newTopRaid) - set(oldTopRaid))
        fallenMembersRaid = list(set(oldTopRaid) - set(newTopRaid))
        api.ribbon6(newMembersRaid, fallenMembersRaid)
        
        newMembersQuest = list(set(newTopQuest) - set(oldTopQuest))
        fallenMembersQuest = list(set(oldTopQuest) - set(newTopQuest))
        api.ribbon7(newMembersQuest, fallenMembersQuest)
        
        if newTopEarner != oldTopEarner:
            api.ribbon8(newTopEarner, oldTopEarner)
        
        def trend(old, new):
            if old > new:
                return 1, new
            if old < new:
                return -1, new
            if old == new:
                return 0, new
        
        for i in range(len(self.leaderboard)):
            oldRank = self.leaderboard.loc[i, "memberRank"]
            if i == 0:
                if oldRank == None:
                    oldRank = 1 
                newTrend, newRank = trend(oldRank, 1)
            else:
                if self.leaderboard.loc[i, "memberXP"] == self.leaderboard.loc[i-1, "memberXP"]:
                    if oldRank == None:
                        newTrend, newRank = trend(self.leaderboard.loc[i-1, "memberRank"], self.leaderboard.loc[i-1, "memberRank"])
                    else:
                        newTrend, newRank = trend(oldRank, self.leaderboard.loc[i-1, "memberRank"])
                else:
                    if oldRank == None:
                        newTrend, newRank = trend(i+1, i+1)
                    else:
                        newTrend, newRank = trend(oldRank, i+1)
                   
            self.leaderboard.loc[i, "memberRank"] = newRank
            self.leaderboard.loc[i, "trend"] = newTrend
        
        memXP = self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["memberXP"][0]
        return self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["memberRank"][0], self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["trend"][0], memXP, self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["servers"][0]
            
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
    def __init__(self, sID):
        ## init an empty pandas dataframe with the following columns:
        ## memberID, memberXP, memberRank, trend
        self.serverID = sID
        self.leaderboard = pd.DataFrame(columns = ["memberID", "memberXP", "memberRank", "trend", "questXP", "raidXP"])
    
    def update(self, memberID, XP, quest = False, raid = False):
        
        try:
            oldTopQuest = self.leaderboard.loc[self.leaderboard["questXP"] == self.leaderboard["questXP"].max(), "memberID"]
            oldTopRaid = self.leaderboard.loc[self.leaderboard["raidXP"] == self.leaderboard["raidXP"].max(), "memberID"]
        except:
            oldTopQuest, oldTopRaid = [], [], []
        
        try:
            oldTopEarner = self.leaderboard["memberID"].iloc[0]
        except:
            oldTopEarner = None
        
        
        if memberID in list(self.leaderboard["memberID"]):
            self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "memberXP"]
            if quest:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "questXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "questXP"]
            elif raid:
                self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "raidXP"] = XP + self.leaderboard.loc[self.leaderboard["memberID"] == memberID, "raidXP"]
        else:
            if quest:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame({"memberID":[memberID], "memberXP":[XP], "memberRank":[None], "trend":[0], "questXP":[XP], "raidXP":[0]})], ignore_index = True)
            elif raid:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame({"memberID":[memberID], "memberXP":[XP], "memberRank":[None], "trend":[0], "questXP":[0], "raidXP":[XP]})], ignore_index = True)
            else:
                self.leaderboard = pd.concat([self.leaderboard, pd.DataFrame({"memberID":[memberID], "memberXP":[XP], "memberRank":[None], "trend":[0]})], ignore_index = True)
            
        self.leaderboard = self.leaderboard.sort_values(by = ["memberXP"], ascending = False)
        self.leaderboard = self.leaderboard.reset_index(drop = True)
        
        
        try:
            newTopEarner = self.leaderboard["memberID"].iloc[0]
        except:
            newTopEarner = None
            
        try:
            newTopQuest = self.leaderboard.loc[self.leaderboard["questXP"] == self.leaderboard["questXP"].max(), "memberID"]
            newTopRaid = self.leaderboard.loc[self.leaderboard["raidXP"] == self.leaderboard["raidXP"].max(), "memberID"]
        except:
            newTopQuest, newTopRaid = [], [], []
            
        if self.serverID != None and newTopEarner != oldTopEarner:
            api.ribbon5(newTopEarner, oldTopEarner, self.serverID)
            
        newMembersRaid = list(set(newTopRaid) - set(oldTopRaid))
        fallenMembersRaid = list(set(oldTopRaid) - set(newTopRaid))
        api.ribbon3(newMembersRaid, fallenMembersRaid, self.serverID)
        
        newMembersQuest = list(set(newTopQuest) - set(oldTopQuest))
        fallenMembersQuest = list(set(oldTopQuest) - set(newTopQuest))
        api.ribbon4(newMembersQuest, fallenMembersQuest, self.serverID)
        
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
            if i == 0:
                if oldRank == None:
                    oldRank = 1 
                newTrend, newRank = trend(oldRank, 1)
            else:
                if self.leaderboard.loc[i, "memberXP"] == self.leaderboard.loc[i-1, "memberXP"]:
                    if oldRank == None:
                        newTrend, newRank = trend(self.leaderboard.loc[i-1, "memberRank"], self.leaderboard.loc[i-1, "memberRank"])
                    else:
                        newTrend, newRank = trend(oldRank, self.leaderboard.loc[i-1, "memberRank"])
                else:
                    if oldRank == None:
                        newTrend, newRank = trend(i+1, i+1)
                    else:
                        newTrend, newRank = trend(oldRank, i+1)
                   
            self.leaderboard.loc[i, "memberRank"] = newRank
            self.leaderboard.loc[i, "trend"] = newTrend
            
        return self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["memberRank"][0], self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["trend"][0], self.leaderboard.loc[self.leaderboard["memberID"] == memberID].reset_index()["memberXP"][0]
            
    def search(self, string):
        ## search all member IDs for string, returning all values of the leaderboard for match
        ## for example, the string "ABC" would return all rows with memberID containing "ABC"
        return self.leaderboard[self.leaderboard["memberID"].str.contains(string)]
    
    def top3(self):
        ## return a list of the top 3 members, in this format: 
        ## [MemberID, Rank, XP]
        ## if there are less than 3 members, return all members
        top3 = []
        for i in range(len(self.leaderboard)):
            if i == 0:
                top3 = [[self.leaderboard.loc[i, "memberID"], self.leaderboard.loc[i, "memberRank"], self.leaderboard.loc[i, "memberXP"]]]
            elif i == 1:
                top3.append([self.leaderboard.loc[i, "memberID"], self.leaderboard.loc[i, "memberRank"], self.leaderboard.loc[i, "memberXP"]])
            elif i == 2:
                top3.append([self.leaderboard.loc[i, "memberID"], self.leaderboard.loc[i, "memberRank"], self.leaderboard.loc[i, "memberXP"]])
            else:
                break
        return top3
        
    
    def reprJSON(self):
        return self.leaderboard.to_dict(orient = "records")
    
    def getRankTrendXP(self, memberID):
        row = self.leaderboard[self.leaderboard["memberID"] == memberID]
        rank = row["memberRank"].values[0]
        trend = row["trend"].values[0]
        XP = row["memberXP"].values[0]
        return rank, trend, XP
    
class jackpot:
    def __init__(self, amount, deadline, winners, servers, members):
        self.jackpot = "2500"
        ##self.deadline = datetime.now() + pd.Timedelta(days = 30)
        self.winners = 7
        self.deadline = "Feb 22nd @ 9:00pm EST"
        self.servers = 0
        self.members = 0
    
    def update(self, amount):
        self.jackpot += amount
    
    def getJackpot(self):
        return self.jackpot
    
    def resetJackpot(self):
        self.jackpot = 0
    
    def reprJSON(self):
        return {"jackpot": self.jackpot, "deadline": self.deadline.strftime("%Y-%m-%d %H:%M:%S")}

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