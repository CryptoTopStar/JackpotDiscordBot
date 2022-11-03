import requests
token = "dvdNNA7oUx2bmI8R8TbpkWLGe"
token_secret = "s0EMFs1jCh74t7nD5rB6SxoXTdmq5T3qpScqfv27LuUijsov1j"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANWrigEAAAAAM6iZitFfLe9t5zNuLjj8Bd9JSOk%3DvTZBnHaUWgyHlMkJj6V2r44gbRWy53LyLJidUcmucXK1xHUKL8"

## tweet test case
tweet_id = 1578084770172600322

## use the Twitter API to check if a specific user retweeted a specific tweet
retweeter = "@klimkowskio"
def checkRetweet(tweet_id, retweeter):
    url = "https://api.twitter.com/2/tweets/{}/retweeted_by".format(tweet_id)
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"user.fields": "username"}
    response = requests.request("GET", url, headers=headers, params=params)
    users = response.json()["data"]
    for user in users:
        if user["username"] == retweeter[1:]:
            return True
    return False

checkRetweet(tweet_id, retweeter) ## returns True
checkRetweet(tweet_id, "somerandomID") ## returns False

## use the Twitter API to check if a specific user liked a specific tweet
liker = "@Kokren69"
def checkLike(tweet_id, liker):
    url = "https://api.twitter.com/2/tweets/{}/liking_users".format(tweet_id)
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"user.fields": "username"}
    response = requests.request("GET", url, headers=headers, params=params)
    users = response.json()["data"]
    for user in users:
        if user["username"] == liker[1:]:
            return True
    return False

checkLike(tweet_id, retweeter) ## returns True
checkLike(tweet_id, "somerandomID") ## returns False

## check the relationship between two users using the Twitter API 1.1
mainUser = "@Google"
follower = "@kusbiscuits" ## if this person is following the main user, return true
def checkRelashionship(mainUser, follower):
    url = "https://api.twitter.com/1.1/friendships/show.json"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"source_screen_name": mainUser[1:], "target_screen_name": follower[1:]}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    if result["relationship"]["target"]["following"] == True:
        return True
    return False

## check to see if the last tweet of a user is a retweet 
## of a specific tweet 
user = "@Shubham99925933"
def checkRetweetOf(tweet_id, user):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"screen_name": user[1:], "count": 1}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    try:
        if result[0]["retweeted_status"]["id"] == tweet_id:
            return True
    except:  
        return False

    return False
    
