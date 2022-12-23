import requests
bot_token = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"

## use the discord API to check if a specific user reacted to a specific message
def checkReact(user, message):
    url = "https://discord.com/api/v8/channels/{}/messages/{}".format(message.channel.id, message.id)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    for reaction in result["reactions"]:
        for user in reaction["users"]:
            if user["id"] == "ID":
                return True
    return False

## use the discord API to check if a specific user replied to a specific message
def checkReply(user, message):
    url = "https://discord.com/api/v8/channels/{}/messages/{}".format(message.channel.id, message.id)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    for reply in result["message_reference"]["message_id"]:
        if reply["author"]["id"] == "ID":
            return True
    return False

## use the discord API to check the total number of messages a user has sent in all channels
def messagesSent(user):
    url = "https://discord.com/api/v8/users/{}/messages/search".format(user.id)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    params = {"author_id": user.id}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    return result["total_results"]

## total number of reactions a user has sent in a specific channel
def reactionsMade(user):
    url = "https://discord.com/api/v8/users/{}/messages/search".format(user.id)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    params = {"author_id": user.id}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    total = 0
    for message in result["messages"]:
        for reaction in message["reactions"]:
            total += reaction["count"]
    return total

## see if the user has been active in the last 24 hours
def isActive(user):
    url = "https://discord.com/api/v8/users/{}/messages/search".format(user)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    params = {"author_id": user}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    for message in result["messages"]:
        if message["timestamp"] > "24 hours ago":
            return True
    return False

## see if the user interacts with a specific user
def interactsWith(user, target):
    url = "https://discord.com/api/v8/users/{}/messages/search".format(user.id)
    headers = {"Authorization": "Bot {}".format(bot_token)}
    params = {"author_id": user.id}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    for message in result["messages"]:
        if message["author"]["id"] == target.id:
            return True
    return False

