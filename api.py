import csv
from datetime import datetime
from leadboardLogic import User, TwitterRaid, Mission, Server, globalLeaderboard, serverLeaderboard, jackpot, Member
import random
import string
import json
import os
import math
import pickle

jackpotObjects = [jackpot()]

## SCHEMA:
##      - KEY: Community Server ID
##      - VALUE: MEMBER_DICT
##               - KEY: Member Name/ID
##               - VALUE: Member Object
optIn = {}

## SCHEMA:
##      - KEY: Community Server ID
##      - VALUE: LIST (TWITTER RAID OBJECTS)
##               - .link: str --> link to the tweet
##               - .date: date --> when the tweet raid was made
##               - .boosted: bool --> if the tweet was boosted
##               - .retweet: bool --> if raid includes retweets
##               - .react: bool --> if raid includes reactions
##               - .comment: bool --> if raid includes comments
##               - .completed: dict --> 
##                      - KEY: Member Name/ID
##                      - VALUE: list --> 
##                             -  ["reaction" (optional), "comment" (optional), "retweet" (optional)] representing reaction, comment, and retweet
twitterRaids = {}
missions = {}

## SCHEMA:
##     - KEY: Community Server ID
##     - VALUE: LOG_LIST
##        - [0]: Member Name/ID
##        - [1]: Task Type
##        - [2]: XP Override
##        - [3]: Task Time
logs = {}

## SCHEMA:
##     - KEY: Community Server ID
##     - VALUE: INDIVIDUAL_WEIGHTS_DICT
##               - KEY: Member Name/ID
##               - VALUE: Member Weight
INDIVIDUAL_WEIGHTS = {}

## SCHEMA:
##     - KEY: Community Server ID
##     - VALUE: Community Weight
COMMUNITY_WEIGHT = {}

## SCHEMA:
##    - KEY: Community Server ID
##    - VALUE: Server Object
SERVERS = {}

## SCHEMA:
##   - KEY: Community Server Name
##   - VALUE: Community Server ID
SERVER_NAMES = {}

DEFAULT_WEIGHT = 1
XP_AWARDS = {0:1000, 1:40, 2:15, 3:200, 4:800, 5:700, -5:-700, 6:500, 7:1000, 8:400, 9:150, 10:600, 11:200, 12:400, 13:1200, 14:400, 15:800, 16:0, 17:3500, 18:3600, 19:4000, 20:5000, 21:0}
GLOBAL = globalLeaderboard()

## SCHEMA:
##    - KEY: Referal Code
##    - VALUE: [SERVER ID, MEMBER OBJECT]
referalCode = {}

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
        
def convertToDict(dictObj):
    ## this dict could have other dicts as values with nested class objects. Convert the nested class objects to dicts as well, storing them in a new dict
    ## to convert class object to dict, use obj.reprJSON()
    
    ## if the object is not a dictionary, return it
    if not isinstance(dictObj, dict):
        return dictObj.reprJSON()
    
    data = {}
    for key in dictObj.keys():
        ## if the value is a dictionary, convert it to a dict:
        if isinstance(dictObj[key], dict):
            data[key] = convertToDict(dictObj[key])
        ## if its a list, int, str, etc. just add it to the dict
        elif isinstance(dictObj[key], list) or isinstance(dictObj[key], int) or isinstance(dictObj[key], str) or isinstance(dictObj[key], bool):
            data[key] = dictObj[key]
        else:
            data[key] = dictObj[key].reprJSON()
    return data

def saveObject(obj, name):
    ## if 'Cache/Objects/' + name + '.json' doesn't exist, create it
    if not os.path.exists('Cache/Objects/' + name + '.json'):
        open('Cache/Objects/' + name + '.json', 'w').close()
        
    with open('Cache/Objects/' + name + '.json', 'w') as f:
        ## if the object is a dictionary, save it as a JSON
        if isinstance(obj, dict):
            json.dump(convertToDict(obj), f)
        else:
            ## save a class object with all of its attributes as a JSON. If the attribute is a class object, save that as well
            json.dumps(obj.reprJSON(), cls=ComplexEncoder)

def saveMissions():
    def refresh(missions):
        data = {}
        names = {}
        for ids in missions.keys():
            data[ids] = []
            serverName = SERVERS[ids].name
            serverName = serverName.lower().replace(" ", "")
            names[ids] = serverName
        for ids in missions.keys():
            for mission in missions[ids]:
                data[ids].append(missions[ids][mission].title)
        data["names"] = names
        return data
    
    with open('Cache/missions.json', 'w') as f:
        json.dump(refresh(missions), f)

def basicMissions(serverID):
    #DEPRECATED FOR NOW: buy the floor, sweep the floor, set your pfp to the project's nft, retweet pinned tweet
    createMission(serverID, "Tweet about the project", "Post a Tweet from your personal Twitter account that tags the project. Submit the link or a screenshot as proof.", 2000)
    createMission(serverID, "Become a server booster", "Boost the server. Submit a screenshot as proof.", 3000)
    createMission(serverID, "Give another community member a shoutout on Twitter", "Post a Tweet from your personal Twitter account that recognizes another community member for their community contributions. Submit the link or a screenshot as proof.", 3500)
    createMission(serverID, "Write a thread about the project on Twitter", "Post a Twitter Thread from your personal Twitter account that tags the project. Submit the link or a screenshot as proof.", 3500)
    # createMission(serverID, "Buy the floor", "Purchase one of the NFT’s with the current floor price", 3000)
    # createMission(serverID, "Sweep the floor", "Purchase a minimum of 3 NFT’s on the current floor ", 7500)
    # createMission(serverID, "Set your PFP to the project’s NFT", "Change your Twitter profile picture to your NFT", 4000)
    createMission(serverID, "Add the project’s handle to your twitter bio", "Add the project’s handle to your Twitter bio. Submit a link to your profile or a screenshot of your bio as proof.", 4000)
    createMission(serverID, "Add project-inspired banner to your Twitter profile", "Change your Twitter banner to any image related to the project. Submit a link to your profile or a screenshot of your profile as proof.", 3500)
    createMission(serverID, "Talk about the project in another server", "Mention the project in another community’s Discord Server. Submit a screenshot of the interaction as proof.", 2000)
    # createMission(serverID, "Have a 10 minute call", "Have a 10 minute call via Discord, phone, Google Meet, or some other form of call, with another member of the community ", 2500)
    # createMission(serverID, "Introduce an idea for Missions", "Come up with an idea for a new Mission and share it with an Admin, if it is implemented submit proof.", 1500)
    createMission(serverID, "Join Twitter Spaces", "Join Twitter Spaces hosted by the project or the community. Submit a link to the spaces and a screenshot of your attendance as proof.", 2000)
    createMission(serverID, "Host Twitter Spaces", "Host Twitter Spaces for members of the community. The Spaces should have at least 5 attendees. Submit a link to the spaces and a screenshot of attendees as proof.", 5000)
    createMission(serverID, "Create a YouTube video", "Create a Public Youtube video that relates to the project in some way. Submit a link to the video as proof.", 4000)
    createMission(serverID, "Create a meme", "Create an original meme that relates to the project in some way. Submit the image as proof.", 3500)
    # createMission(serverID, "Retweet the pinned Tweet", "Retweet from your personal account the project’s pinned Tweet", 3600)
    createMission(serverID, "Make fan art", "Create an original graphic or fan art that relates to the project in some way. Submit the image as proof.", 3500)
    # createMission(serverID, "Write a blog post", "Write an online blog post, more than 500 words, that relates to the project in someway", 4000)
    createMission(serverID, "Follow the project on Twitter", "Follow the project from your personal Twitter account. Submit a screenshot as proof.", 1000)

def addServer(serverID, serverName, url, invites):
    if serverID not in SERVERS:
        SERVERS[serverID] = Server(serverName, serverID, url, invites)
        SERVER_NAMES[serverName] = serverID
        jackpotObjects[len(jackpotObjects) - 1].servers += 1
        basicMissions(serverID)
        saveObject(SERVERS, "SERVERS")
        saveObject(SERVER_NAMES, "SERVER_NAMES")
        return True
    else:
        return False

def getServerDeadline(serverID):
    try:
        return SERVERS[serverID].endDate
    except:
        return None

def updateInvites(serverID, invites):
    try:
        SERVERS[serverID].invites = invites
        saveObject(SERVERS, "SERVERS")
        return True
    except:
        return False

def getInvites(serverID):
    try:
        return SERVERS[serverID].invites
    except:
        return None

def setServerEndMessage(serverID, messageID):
    ## messageID: [missionMes, raidMes]
    try:
        SERVERS[serverID].endMessage = messageID
        return True
    except:
        return None
    
def getServerEndMessage(serverID):
    ## messageID: [missionMes, raidMes]
    try:
        return SERVERS[serverID].endMessage
    except:
        return None

def checkOptIn(serverID, memberName):
    if serverID not in optIn:
        return False
    if memberName not in optIn[serverID]:
        return False
    return optIn[serverID][memberName]

def returnXP(serverID, memberName):
    return optIn[serverID][memberName].finalXP

def optInMember(serverID, memberID, fullIdentifier, memberName, url, tweetOBJ = None, wallet = None):
    if serverID not in optIn:
        optIn[serverID] = {}
    SERVERS[serverID].optInCount = SERVERS[serverID].optInCount + 1
    jackpotObjects[len(jackpotObjects) - 1].members += 1
    if memberName not in optIn[serverID]:
        optIn[serverID][memberID] = User(memberName, fullIdentifier, memberID, serverID, url, tweetOBJ, wallet)
        saveObject(optIn, "optIn")
        return True
    else:
        return False

def getMember(serverID, memberName):
    if serverID not in optIn:
        return None
    if memberName not in optIn[serverID]:
        return None
    return optIn[serverID][memberName]
    
def addLogEvent(serverID, memberName, taskType, xpOverride = None):
    if serverID not in logs:
        logs[serverID] = []
        
    if xpOverride == None:
        xpORDValue = "NONE"
    else:
        xpORDValue = xpOverride
        
    ## get the current time in this format: "%m/%d/%y %H:%M"
    realTimeDate = datetime.now().strftime("%m/%d/%y %H:%M")
    
    point = [str(memberName), str(taskType), str(xpORDValue), str(realTimeDate)]
    logs[serverID].append(point)
    saveObject(logs, "logs")
    return point

def calXP(memberObject):
    xp = 0
    for key, value in memberObject.counter.items():
        if key == 1:
            xp += messageXP(value)
        elif key == 2:
            xp += reactXP(value)
        elif key == 5:
            count = value - memberObject.counter[-5]
            if count <= 0:
                continue
            else:
                xp += inviteXP(count)
        elif key == -5:
            continue
        else:
            xp += value * XP_AWARDS[key]
    return xp

def deleteTwitterRaid(serverID, raidID):
    if serverID not in twitterRaids:
        return False
    if raidID not in twitterRaids[serverID]:
        return False
    del twitterRaids[serverID][raidID]
    return True

def createTwitterRaid(serverID, title, link, boosted, retweet, react, comment):
    if serverID not in twitterRaids:
        twitterRaids[serverID] = {}
    
    raidObject = TwitterRaid(title, link, boosted, retweet, react, comment)
    
    randID = random.randint(4000, 100000000000)
    while randID in twitterRaids[serverID].keys():
        randID = random.randint(4000, 100000000000)
    
    twitterRaids[serverID][randID] = raidObject
    saveObject(twitterRaids, "twitterRaids")
    return randID

def retMissions():
    return missions

def createMission(serverID, name, discp, reward, suppy = "", perperson = ""):
    if serverID not in missions:
        missions[serverID] = {}
        
    if suppy == "":
        suppy = None
    if perperson == "":
        perperson = None
        
    missionObject = Mission(name, discp, int(reward), suppy, perperson)
    
    randID = random.randint(4000, 100000000000)
    while randID in missions[serverID].keys():
        randID = random.randint(4000, 100000000000)
    
    missions[serverID][randID] = missionObject
    saveMissions()
    saveObject(missions, "missions")
    return randID

def getMissionXP(serverID, missionID):
    if serverID not in missions:
        return 0
    
    return missions[serverID][missionID].xp

def getNumMissionSubmissions(serverID, missionID, memberName):
    try:
        return len(missions[serverID][missionID].completed[memberName])
    except:
        return 0

def getMissions(serverID):
    ## schema: [Mission Name, Mission Description, Mission Reward, Mission Supply, Mission Count, Mission ID]
    if serverID not in missions:
        return []
    
    retList = []
    for missionID in missions[serverID]:
        missionObjct = missions[serverID][missionID]
        retList.append([missionObjct.title, missionObjct.description, missionObjct.xp, missionObjct.limit, missionObjct.count, missionID, missionObjct.personLimit])
    
    return retList

def getMission(serverID, missionName):
    if serverID not in missions:
        return None
    
    for missionID in missions[serverID]:
        if missions[serverID][missionID].title == missionName:
            return missionID, missions[serverID][missionID]
    
    return None

def deleteMission(serverID, missionID):
    if serverID not in missions:
        return False
    if missionID not in missions[serverID]:
        return False
    del missions[serverID][missionID]
    saveMissions()
    return True

def tweetEventRetweet(serverID, memberName, raidID):
    if serverID not in twitterRaids:
        return "This tweet raid no longer exist"
    if raidID not in twitterRaids[serverID]:
        return "This tweet raid no longer exist"
    else: 
        isBoosted = twitterRaids[serverID][raidID].boosted
    if twitterRaids[serverID][raidID].retweet == False:
        return "This tweet is not eligible for retweet XP rewards"
    if memberName not in twitterRaids[serverID][raidID].completed:
        twitterRaids[serverID][raidID].completed[memberName] = []
    if "retweet" in twitterRaids[serverID][raidID].completed[memberName]:
        return "You have already earned XP for retweeting this tweet"
    else:
        twitterRaids[serverID][raidID].completed[memberName].append("retweet")
        if isBoosted:
            points = xpEvent(serverID, memberName, 13, xpOverride = None)
        else:
            points = xpEvent(serverID, memberName, 10, xpOverride = None)
    return points

def tweetEventReact(serverID, memberName, raidID):
    if serverID not in twitterRaids:
        return "This tweet raid no longer exist"
    if raidID not in twitterRaids[serverID]:
        return "This tweet raid no longer exist"
    else: 
        isBoosted = twitterRaids[serverID][raidID].boosted
    if twitterRaids[serverID][raidID].react == False:
        return "This tweet is not eligible for react XP rewards"
    if memberName not in twitterRaids[serverID][raidID].completed:
        twitterRaids[serverID][raidID].completed[memberName] = []
    if "react" in twitterRaids[serverID][raidID].completed[memberName]:
        return "You have already earned XP for reacting to this tweet"
    else:
        twitterRaids[serverID][raidID].completed[memberName].append("react")
        if isBoosted:
            points = xpEvent(serverID, memberName, 14, xpOverride = None)
        else:
            points = xpEvent(serverID, memberName, 11, xpOverride = None)
    return points

def tweetEventComment(serverID, memberName, raidID):
    if serverID not in twitterRaids:
        return "This tweet raid no longer exist"
    if raidID not in twitterRaids[serverID]:
        return "This tweet raid no longer exist"
    else: 
        isBoosted = twitterRaids[serverID][raidID].boosted
    if twitterRaids[serverID][raidID].comment == False:
        return "This tweet is not eligible for comment XP rewards"
    if memberName not in twitterRaids[serverID][raidID].completed:
        twitterRaids[serverID][raidID].completed[memberName] = []
    if "comment" in twitterRaids[serverID][raidID].completed[memberName]:
        return "You have already earned XP for commenting to this tweet"
    else:
        twitterRaids[serverID][raidID].completed[memberName].append("comment")
        if isBoosted:
            points = xpEvent(serverID, memberName, 15, xpOverride = None)
        else:
            points = xpEvent(serverID, memberName, 12, xpOverride = None)
    return points

def getTweetTitle(serverID, raidID):
    return twitterRaids[serverID][raidID].title

def xpEvent(serverID, memberName, taskType, xpOverride = None):
    ## update the event 
    memberObject = getMember(serverID, memberName)
    point = addLogEvent(serverID, memberName, taskType, xpOverride)
    oldXP = memberObject.finalXP
    if oldXP == None:
        oldXP = 0
    if point[2] != "NONE":
        memberObject.xpOverride += int(point[2])
        memberObject.counterOverride[int(point[1])] += 1
    else:
        memberObject.counter[int(point[1])] += 1
    
    ## update the XP value
    weight = DEFAULT_WEIGHT
    if serverID in INDIVIDUAL_WEIGHTS and memberName in INDIVIDUAL_WEIGHTS[serverID]:
        weight *= INDIVIDUAL_WEIGHTS[serverID][memberName]
        
    if serverID in COMMUNITY_WEIGHT:
        weight *= COMMUNITY_WEIGHT[serverID]

    newXP = weight * (calXP(memberObject) + memberObject.xpOverride)
    updateLeaderboards(memberName, serverID, newXP - oldXP)
    memberObject.finalXP = newXP
    
    saveObject(optIn, "optIn")
    saveObject(missions, "missions")
    
    if xpOverride != None:
        return xpOverride
    
    return XP_AWARDS[taskType]

def serverVisit(serverID, memberName):
    memberObject = getMember(serverID, memberName)
    lastActive = datetime.strptime(memberObject.lastActive, "%m/%d/%y %H:%M")
    memberObject.lastActive = datetime.now().strftime("%m/%d/%y %H:%M")
    month = lastActive.month
    day = lastActive.day
    
    saveObject(optIn, "optIn")
    
    ## if lastActive is the same calendar day as today
    if month != datetime.now().month and day != datetime.now().day:
        return True
    
    return False
    
def getReward(server, memberName, taskType, name = None):
    return str(XP_AWARDS[taskType]) + " XP"

def missionXPEvent(serverID, memberName, missionID):
    limit =  missions[serverID][missionID].limit
    personLimit =  missions[serverID][missionID].personLimit
    
    if missions[serverID][missionID].count >= limit:
        return False
    
    if memberName in missions[serverID][missionID].completed and len(missions[serverID][missionID].completed[memberName]) >= personLimit:
        return False
    
    if memberName not in missions[serverID][missionID].completed:
        missions[serverID][missionID].completed[memberName] = []
        missions[serverID][missionID].numPeople += 1
        
    currentTime = datetime.now().strftime("%m/%d/%y %H:%M")
    missions[serverID][missionID].completed[memberName].append(currentTime)
    missions[serverID][missionID].count += 1
    missionReward = getMissionXP(serverID, missionID)
    xpEvent(serverID, memberName, 16, missionReward)
    
    return missionReward

def checkMissionEligibility(serverID, memberName, missionID):
    try:
        limit =  missions[serverID][missionID].limit
        personLimit =  missions[serverID][missionID].personLimit
        
        if int(missions[serverID][missionID].count) >= limit:
            return False
        
        if memberName in missions[serverID][missionID].completed and len(missions[serverID][missionID].completed[memberName]) >= personLimit:
            return False
        
        return True
    except:
        return False

def createAlphaNumericCode(serverID, memberID):
    def createCode():
        code = ""
        for i in range(12):
            if i % 4 == 0 and i != 0:
                code += "-"
            else:
                code += random.choice(string.ascii_uppercase + string.digits)
        return code
    
    refCode = createCode()
    while refCode in referalCode:
        refCode = createCode()
        
    memberObject = optIn[serverID][memberID]
    referalCode[refCode] = [serverID, memberID]
    
    memberObject.referal = refCode
    saveObject(optIn, "optIn")
    saveObject(referalCode, "referalCode")
    return refCode

def updateLeaderboards(memberID, serverID, XP):
    GLOBAL.update(memberID, XP, serverID)
    SERVERS[serverID].leaderboard.update(memberID, XP)
    saveObject(SERVERS, "SERVERS")
    saveObject(GLOBAL, "GLOBAL")
    
def getJackpot():
    return str(jackpotObjects[len(jackpotObjects) - 1].jackpot)

def getJackpotDeadline():
    return str(jackpotObjects[len(jackpotObjects) - 1].deadline)

def getJackpotNumber():
    return str(jackpotObjects[len(jackpotObjects) - 1].servers), str(jackpotObjects[len(jackpotObjects) - 1].members), str(jackpotObjects[len(jackpotObjects) - 1].winners)

def isNew(serverID, memberID, memberInteractionID):
    try:
        if memberID in SERVERS[serverID].newMembers and len(SERVERS[serverID].newMembers[memberID].interactions) < 10 and memberInteractionID not in SERVERS[serverID].newMembers[memberID].interactions:
            SERVERS[serverID].newMembers[memberID].interactions.append(memberInteractionID)
            return True
    except:
        return False

def addNewMember(serverID, name, memberID):
    if memberID not in SERVERS[serverID].newMembers:
        SERVERS[serverID].newMembers[memberID] = Member(name, memberID, serverID)
        saveObject(SERVERS, "SERVERS")
        return SERVERS[serverID].newMembers[memberID]
    else:
        return False

def findNewMember(serverID, memberID):
    if memberID in SERVERS[serverID].newMembers:
        return SERVERS[serverID].newMembers[memberID]
    else:
        return None
    
def getRank(serverID, memberID):
    serverRank, serverTrend, serverXP = SERVERS[serverID].leaderboard.getRankTrendXP(memberID)
    globalRank, __, globalXP = GLOBAL.getRankTrendXP(memberID)
    return serverRank, serverTrend, serverXP, globalRank, globalXP

def messageXP(x): ## code 1
    if x <= 10:
        return 40 * x
    return math.floor(2070.317 + (-11.18103 - 2070.317)/(1 + (x/38.73653)**1.029935) + 4.11)

def reactXP(x): ## code 2
    if x <= 10:
        return 15 * x
    return math.floor(1546.222 + (7.613213 - 1546.222)/(1 + (x/62.02515)**1.249896)-6)

def inviteXP(x): ## code 5
    if x <= 7:
        return (700 * x) - 50 * ((x - 1) ** 2)
    else:
        return 3100 + (100 * (x - 7))
    
def gettingStarted(serverID):
    try:
        return SERVERS[serverID].welcomeMessages[0]
    except:
        return None

def userSettings(serverID):
    try:
        return SERVERS[serverID].welcomeMessages[1]
    except:
        return None
    
def storeGettingStarted(serverID, message):
    try:
        SERVERS[serverID].welcomeMessages[0] = message
        saveObject(SERVERS, "SERVERS")
        return True
    except:
        return False

def storeUserSettings(serverID, message):
    try:
        SERVERS[serverID].welcomeMessages[1] = message
        saveObject(SERVERS, "SERVERS")
        return True
    except:
        return False
    
def getTop3(serverID):
    return SERVERS[serverID].leaderboard.top3()

def pickleAll():
    if not os.path.exists("./Cache/Backup"):
        os.makedirs("./Cache/Backup")
    try:
        pickle.dump(jackpotObjects, open("./Cache/Backup/jackpot.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(optIn, open("./Cache/Backup/optIn.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(twitterRaids, open("./Cache/Backup/twitterRaids.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(missions, open("./Cache/Backup/missions.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(logs, open("./Cache/Backup/logs.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(INDIVIDUAL_WEIGHTS, open("./Cache/Backup/INDIVIDUAL_WEIGHTS.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(COMMUNITY_WEIGHT, open("./Cache/Backup/COMMUNITY_WEIGHT.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(SERVERS, open("./Cache/Backup/SERVERS.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(SERVER_NAMES, open("./Cache/Backup/SERVER_NAMES.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(GLOBAL, open("./Cache/Backup/GLOBAL.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(DEFAULT_WEIGHT, open("./Cache/Backup/DEFAULT_WEIGHT.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(XP_AWARDS, open("./Cache/Backup/XP_AWARDS.pickle", "wb"))
    except:
        pass
    try:
        pickle.dump(referalCode, open("./Cache/Backup/referalCode.pickle", "wb"))
    except:
        pass

def loadAll():
    if os.path.exists("./Cache/Backup"):
        jackpotObjects = pickle.load(open("./Cache/Backup/jackpot.pickle", "rb"))
        optIn = pickle.load(open("./Cache/Backup/optIn.pickle", "rb"))
        twitterRaids = pickle.load(open("./Cache/Backup/twitterRaids.pickle", "rb"))
        missions = pickle.load(open("./Cache/Backup/missions.pickle", "rb"))
        logs = pickle.load(open("./Cache/Backup/logs.pickle", "rb"))
        INDIVIDUAL_WEIGHTS = pickle.load(open("./Cache/Backup/INDIVIDUAL_WEIGHTS.pickle", "rb"))
        COMMUNITY_WEIGHT = pickle.load(open("./Cache/Backup/COMMUNITY_WEIGHT.pickle", "rb"))
        SERVERS = pickle.load(open("./Cache/Backup/SERVERS.pickle", "rb"))
        SERVER_NAMES = pickle.load(open("./Cache/Backup/SERVER_NAMES.pickle", "rb"))
        GLOBAL = pickle.load(open("./Cache/Backup/GLOBAL.pickle", "rb"))
        DEFAULT_WEIGHT = pickle.load(open("./Cache/Backup/DEFAULT_WEIGHT.pickle", "rb"))
        XP_AWARDS = pickle.load(open("./Cache/Backup/XP_AWARDS.pickle", "rb"))
        referalCode = pickle.load(open("./Cache/Backup/referalCode.pickle", "rb"))
    
    
saveMissions()

## ================= ##
## === FLASK API === ##
## ================= ##

import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    ## get the "page" parameter if it exists, otherwise default to 0
    page = flask.request.args.get('page', 0)
    if page.lower() == "all":
        page = -1
    else:
        page = int(page)
    ## get the "search" parameter if it exists, otherwise default to None
    search = flask.request.args.get('search', None)
    ## get the community parameter if it exists, otherwise default to None
    community = flask.request.args.get('community', None)
    serverID = None
    
    if community == None:
        myLeaderboard = GLOBAL
    elif community in SERVER_NAMES:
        serverID = SERVER_NAMES[community]
        myLeaderboard = SERVERS[serverID].leaderboard
    else:
        return flask.jsonify({"error": "Invalid community name"})
        
    if search != None:
        myLeaderboard = myLeaderboard.search(search)
    else:
        myLeaderboard = myLeaderboard.leaderboard
    
    ## myLeaderboard is now a pd.DataFrame   
    if page != -1:
        ## depending on the page, return the appropriate 100 entries. For example, page 0 returns entries 0-99, page 1 returns entries 100-199, etc.
        ## if the page is out of range, return an empty pd.DataFrame with the same columns as myLeaderboard
        if page * 100 >= len(myLeaderboard):
            myLeaderboard = myLeaderboard.iloc[0:0]
        else:
            myLeaderboard = myLeaderboard.iloc[page * 100:(page + 1) * 100]
            
    def convertToResponseGlobal(myLeaderboard):
        finalResp = {"users": [], "communities": {}}
        def createCommunityObject(serverID):
            name = SERVERS[serverID].name
            profileLink = SERVERS[serverID].pfp
            return {"name": name, "profileLink": profileLink}
        
        for indID in SERVERS:
            finalResp["communities"][indID] = createCommunityObject(indID)
        
        def createUserObject(userName, XP, trend, servers, badges):
            listofIDs = servers.keys().tolist()
            primaryServerID = listofIDs[0]
            profileLink = optIn[primaryServerID][userName].pfp
            twitter = optIn[primaryServerID][userName].handle
            
            return {"userName": userName, "xp": XP, "profileLink":profileLink, "twitter":twitter,"trend":trend, "badges": badges, "community": listofIDs}
        
        for rows in myLeaderboard.iterrows():
            row = rows[1]
            finalResp["users"].append(createUserObject(row["memberID"], row["memberXP"], row["trend"], row["servers"], row["badges"]))
        
        return finalResp
    
    def convertToResponseServer(myLeaderboard, serverID):
        finalResp = {"users": [], "communities": {}}
        def createCommunityObject(serverID):
            name = SERVERS[serverID].name
            profileLink = SERVERS[serverID].pfp
            return {"name": name, "profileLink": profileLink}
        
        finalResp["communities"][serverID] = createCommunityObject(serverID)
        
        def createUserObject(userName, XP, trend, serverID):
            listofIDs = [serverID]
            profileLink = optIn[serverID][userName].pfp
            twitter = optIn[serverID][userName].handle
            badges = GLOBAL.leaderboard.loc[GLOBAL.leaderboard["memberID"] == userName, "badges"].iloc[0]
            
            return {"userName": userName, "xp": XP, "profileLink":profileLink, "twitter":twitter,"trend":trend, "badges": badges, "community": listofIDs}
        
        for rows in myLeaderboard.iterrows():
            row = rows[1]
            finalResp["users"].append(createUserObject(row["memberID"], row["memberXP"], row["trend"], serverID))
            
        return finalResp
        
    
    if community == None:
        return flask.jsonify(convertToResponseGlobal(myLeaderboard))
    else:
        return flask.jsonify(convertToResponseServer(myLeaderboard, serverID))
    
## start the flask app, port 5000
##app.run(port=5000)
    
