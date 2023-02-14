import psycopg2
import random


def connectanddo(commands, args = None):

    conn = psycopg2.connect(database="defaultdb",
                                host="db-postgresql-sfo3-06312-do-user-13128182-0.b.db.ondigitalocean.com",
                                user="doadmin",
                                password="AVNS_-f7ufstYFNsmlNoq3SQ",
                                port="25060")

    sql = conn.cursor()
    
    for i, command in enumerate(commands):
        try:
            if args != None and args[i] != None:
                sql.execute(command, args[i])
            else:
                sql.execute(command)
            conn.commit()
        except:
            try:
                print("Error: " + command, args[i])
            except:
                print("Error: " + command)
            conn.rollback()
            
    conn.commit()
    sql.close()
    conn.close()
    
def setup():
    commands = []
    ## crate a userInfo table with the following information: userID, serverID, referalCode, walletID, twitter handle, pfp link
    commands.append("CREATE TABLE userinfo (user_id VARCHAR(255), server_id VARCHAR(255), ref_code VARCHAR(255), wallet_id VARCHAR(255), twitter_handle VARCHAR(255), pfp_link VARCHAR(1000))")
    ## create a leaderboard table with the following information: "memberID", "memberXP", "memberRank", "trend", "servers", "badges"
    ## servers is a dict of serverID: xp for that server
    ## badges is a list of strings
    commands.append("CREATE TABLE leaderboard (member_id VARCHAR(255), member_xp VARCHAR(255), member_rank VARCHAR(255), trend VARCHAR(255), servers VARCHAR(1000), badges VARCHAR(255))")
    commands.append("CREATE TABLE gleaderboard (member_id VARCHAR(255), member_xp VARCHAR(255), member_rank VARCHAR(255), trend VARCHAR(255), servers VARCHAR(1000), badges VARCHAR(255))")
    ## create a missions table with the following info "missionID", "missionName", "userID", "serverID", "missionXP", "mission discription", "mission contents", "missionStatus"
    commands.append("CREATE TABLE missions (mission_id VARCHAR(255), mission_name VARCHAR(255), user_id VARCHAR(255), server_id VARCHAR(255), mission_xp VARCHAR(255), mission_discription VARCHAR(1000), mission_contents VARCHAR(10000), mission_status VARCHAR(50))")
    ## create a serverInfo table with the following information: serverID, serverName, serverPfp link
    commands.append("CREATE TABLE serverinfo (server_id VARCHAR(255), server_name VARCHAR(255), server_pfp_link VARCHAR(1000))")
    
    connectanddo(commands)
    print("Database setup complete")

def encode(server_id):
    myMap = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"j"}
    encodedStr = ""
    for char in str(server_id):
        encodedStr += myMap[int(char)]
    return encodedStr

def decode(encodedStr):
    myMap = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9}
    decodedStr = ""
    for char in encodedStr:
        decodedStr += myMap[char]
    return decodedStr

def setupServerTable(server_id, server_name, server_pfp_link):
    commands, args = [], []
    commands.append("CREATE TABLE "+str(encode(server_id))+" (member_id VARCHAR(255), member_xp VARCHAR(255), member_rank VARCHAR(255), trend VARCHAR(255), xp_distiled VARCHAR(500), badges VARCHAR(255))")
    commands.append("CREATE TABLE "+"g" + str(encode(server_id))+" (member_id VARCHAR(255), member_xp VARCHAR(255), member_rank VARCHAR(255), trend VARCHAR(255), xp_distiled VARCHAR(500), badges VARCHAR(255))")
    args.append(None)
    commands.append("INSERT INTO serverinfo (server_id, server_name, server_pfp_link) VALUES (%s, %s, %s)")
    args.append((server_id, server_name, server_pfp_link))
    
    connectanddo(commands, args)
    print("done", encode(server_id))
    
def delete(password, server_ids):
    commands = []
    if password == "password":
        commands.append("DROP TABLE userinfo")
        commands.append("DROP TABLE leaderboard")
        commands.append("DROP TABLE missions")
        commands.append("DROP TABLE serverInfo")
        for server_id in server_ids:
            commands.append("DROP TABLE " + str(encode(server_id)))
        connectanddo(commands)
        print("All tables deleted")
    else:
        print("Incorrect password")
        
def add_user(user_id, server_id, twitter_handle, pfp_link, wallet_id = "NONE", ref_code = "NONE"):
    commands, args = [], []
    commands.append("INSERT INTO userinfo (user_id, server_id, ref_code, wallet_id, twitter_handle, pfp_link) VALUES (%s, %s, %s, %s, %s, %s)")
    args.append((user_id, str(server_id), ref_code, wallet_id, twitter_handle, pfp_link))
    connectanddo(commands, args)
    
def add_wallet(user_id, server_id, wallet_id):
    commands, args = [], []
    commands.append("UPDATE userinfo SET wallet_id = %s WHERE user_id = %s AND server_id = %s")
    args.append((wallet_id, user_id, str(server_id)))
    connectanddo(commands, args)
    
def add_ref_code(user_id, server_id, ref_code):
    commands, args = [], []
    commands.append("UPDATE userinfo SET ref_code = %s WHERE user_id = %s AND server_id = %s")
    args.append((ref_code, user_id, str(server_id)))
    connectanddo(commands, args)
    
def add_mission(mission_id, mission_name, user_id, server_id, mission_xp, mission_discription, mission_contents, mission_status = "PENDING"):
    print("NEW MISSIONID:", mission_id)
    commands, args = [], []
    commands.append("INSERT INTO missions (mission_id, mission_name, user_id, server_id, mission_xp, mission_discription, mission_contents, mission_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    args.append((mission_id, mission_name, user_id, str(server_id), mission_xp, mission_discription, mission_contents, mission_status))
    connectanddo(commands, args)
    
def finish_mission(mission_id):
    commands = []
    commands.append("UPDATE missions SET mission_status = 'FINISHED' WHERE mission_id = "+ str(mission_id))
    connectanddo(commands)
    
def leaderboard(member_id, member_xp, member_rank, trend, servers = "{}", badges = "[]"):
    print("MEMXP", str(member_xp))
    conn = psycopg2.connect(database="defaultdb",
                                host="db-postgresql-sfo3-06312-do-user-13128182-0.b.db.ondigitalocean.com",
                                user="doadmin",
                                password="AVNS_-f7ufstYFNsmlNoq3SQ",
                                port="25060")

    sql = conn.cursor()
    
    ## create a leaderboard table with the following information: "memberID", "memberXP", "memberRank", "trend", "servers", "badges"
    ## servers is a dict of serverID: xp for that server
    ## badges is a list of strings
    
    ## if the member is already in the leaderboard, update their info
    sql.execute("SELECT member_id FROM leaderboard")
    myData = sql.fetchone()
    if myData != None and member_id in myData:
        typeCode = "UPDATE leaderboard SET member_xp = %s, member_rank = %s, trend = %s, servers = %s, badges = %s WHERE member_id = %s"
        sql.execute(typeCode, (member_xp, member_rank, trend, str(servers), badges, member_id))
    else:
        typeCode = "INSERT INTO leaderboard (member_id, member_xp, member_rank, trend, servers, badges) VALUES (%s, %s, %s, %s, %s, %s)"
        sql.execute(typeCode, (member_id, member_xp, member_rank, trend, str(servers), badges))
    
    conn.commit()
    sql.close()
    conn.close()
    
def gleaderboard(member_id, member_xp, member_rank, trend, servers = "{}", badges = "[]"):
    print("MEMXP", str(member_xp))
    conn = psycopg2.connect(database="defaultdb",
                                host="db-postgresql-sfo3-06312-do-user-13128182-0.b.db.ondigitalocean.com",
                                user="doadmin",
                                password="AVNS_-f7ufstYFNsmlNoq3SQ",
                                port="25060")

    sql = conn.cursor()
    
    ## create a leaderboard table with the following information: "memberID", "memberXP", "memberRank", "trend", "servers", "badges"
    ## servers is a dict of serverID: xp for that server
    ## badges is a list of strings
    
    ## if the member is already in the leaderboard, update their info
    sql.execute("SELECT member_id FROM leaderboard")
    myData = sql.fetchone()
    if myData != None and member_id in myData:
        typeCode = "UPDATE gleaderboard SET member_xp = %s, member_rank = %s, trend = %s, servers = %s, badges = %s WHERE member_id = %s"
        sql.execute(typeCode, (member_xp, member_rank, trend, str(servers), badges, member_id))
    else:
        typeCode = "INSERT INTO gleaderboard (member_id, member_xp, member_rank, trend, servers, badges) VALUES (%s, %s, %s, %s, %s, %s)"
        sql.execute(typeCode, (member_id, member_xp, member_rank, trend, str(servers), badges))
    
    conn.commit()
    sql.close()
    conn.close()
    
def serverLeaderboard(member_id, server_id, member_xp, member_rank, trend, xp_distiled = "{}", badges = "[]"):
    conn = psycopg2.connect(database="defaultdb",
                                host="db-postgresql-sfo3-06312-do-user-13128182-0.b.db.ondigitalocean.com",
                                user="doadmin",
                                password="AVNS_-f7ufstYFNsmlNoq3SQ",
                                port="25060")

    sql = conn.cursor()
    typeCode = "SELECT member_id FROM " + encode(server_id)
    sql.execute(typeCode)
    #sql.execute("SELECT member_id FROM " + str(server_id))
    myData = sql.fetchone()
    if myData != None and member_id in myData:
        typeCode = "UPDATE " + str(encode(server_id)) + " SET member_xp = %s, member_rank = %s, trend = %s, xp_distiled = %s, badges = %s WHERE member_id = %s"
        sql.execute(typeCode, (member_xp, member_rank, trend, str(xp_distiled), badges, member_id))
        #sql.execute("UPDATE " + encode(server_id) + " SET member_xp = "+ str(member_xp)+", member_rank = "+ str(member_rank)+", trend = "+ str(trend) +", xp_distiled = "+ str(xp_distiled)+" WHERE member_id = "+ str(member_id))
    else:
        typeCode = "INSERT INTO "+ str(encode(server_id)) +" (member_id, member_xp, member_rank, trend, xp_distiled, badges) VALUES (%s, %s, %s, %s, %s, %s)"
        sql.execute(typeCode, (member_id, member_xp, member_rank, trend, str(xp_distiled), badges))
        #sql.execute("INSERT INTO " + encode(server_id) + " (member_id, member_xp, member_rank, trend, xp_distiled, badges) VALUES ("+ str(member_id)+", "+ str(member_xp)+", "+ str(member_rank)+", "+ str(trend)+", "+ str(xp_distiled) +", "+ str(badges) +")")
    conn.commit()
    sql.close()
    conn.close()
    
def gserverLeaderboard(member_id, server_id, member_xp, member_rank, trend, xp_distiled = "{}", badges = "[]"):
    conn = psycopg2.connect(database="defaultdb",
                                host="db-postgresql-sfo3-06312-do-user-13128182-0.b.db.ondigitalocean.com",
                                user="doadmin",
                                password="AVNS_-f7ufstYFNsmlNoq3SQ",
                                port="25060")

    sql = conn.cursor()
    typeCode = "SELECT member_id FROM g" + encode(server_id)
    sql.execute(typeCode)
    #sql.execute("SELECT member_id FROM " + str(server_id))
    myData = sql.fetchone()
    if myData != None and member_id in myData:
        typeCode = "UPDATE g" + str(encode(server_id)) + " SET member_xp = %s, member_rank = %s, trend = %s, xp_distiled = %s, badges = %s WHERE member_id = %s"
        sql.execute(typeCode, (member_xp, member_rank, trend, str(xp_distiled), badges, member_id))
        #sql.execute("UPDATE " + encode(server_id) + " SET member_xp = "+ str(member_xp)+", member_rank = "+ str(member_rank)+", trend = "+ str(trend) +", xp_distiled = "+ str(xp_distiled)+" WHERE member_id = "+ str(member_id))
    else:
        typeCode = "INSERT INTO g"+ str(encode(server_id)) +" (member_id, member_xp, member_rank, trend, xp_distiled, badges) VALUES (%s, %s, %s, %s, %s, %s)"
        sql.execute(typeCode, (member_id, member_xp, member_rank, trend, str(xp_distiled), badges))
        #sql.execute("INSERT INTO " + encode(server_id) + " (member_id, member_xp, member_rank, trend, xp_distiled, badges) VALUES ("+ str(member_id)+", "+ str(member_xp)+", "+ str(member_rank)+", "+ str(trend)+", "+ str(xp_distiled) +", "+ str(badges) +")")
    conn.commit()
    sql.close()
    conn.close()
    
def pushAll():
    ## delete all rows in the leaderboard table
    ## delete all rows in all the server tables
    return