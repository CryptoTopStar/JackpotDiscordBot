import requests
token = "dvdNNA7oUx2bmI8R8TbpkWLGe"
token_secret = "s0EMFs1jCh74t7nD5rB6SxoXTdmq5T3qpScqfv27LuUijsov1j"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANWrigEAAAAAM6iZitFfLe9t5zNuLjj8Bd9JSOk%3DvTZBnHaUWgyHlMkJj6V2r44gbRWy53LyLJidUcmucXK1xHUKL8"

API_KEY = "ZGUdjkFTWuuVFJYDUHoucR1Ry"
API_KEY_SECRETE = "xfFoq1ynIvsnZ7MeipWGT6XMFUx466i1tIaexUKXfqMmoj9EU1"
PROD_BEARER = "AAAAAAAAAAAAAAAAAAAAAKLIkwEAAAAA0KdfM2HZYg9M5bGXZJrExM2x7sg%3DnBSYpThXPQkgAhq2nXHtelNhkGAWQxtrbx1XM1eEjwEplm3MXX"

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
def checkRelationship(mainUser, follower):
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
def checkRetweetOf(tweet_id, retweeter):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"screen_name": retweeter[1:], "count": 1}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    try:
        if result[0]["retweeted_status"]["id"] == tweet_id:
            return True
    except:  
        return False

    return False

## return the tweet id of the last tweet of a user
def getLastTweetID(user):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    params = {"screen_name": user[1:], "count": 1}
    response = requests.request("GET", url, headers=headers, params=params)
    result = response.json()
    return int(result[0]["id"])
    
## Use Pin based OAuth to get the access token and access token secret
## First, get the redirect URL

def getURL():
    import time
    import uuid
    base_url = "https://api.twitter.com"
    endpoint = "/oauth/request_token"
    url = base_url + endpoint
    oauth_timestamp = str(int(time.time()))
    oauth_nonce = str(uuid.uuid4()).replace("-", "")
    headers = {"Authorization": "OAuth oauth_callback=\"oob\", oauth_consumer_key=\"{}\", oauth_nonce=\"{}\", oauth_signature=\"{}\", oauth_signature_method=\"HMAC-SHA1\", oauth_version=\"1.0\"".format(API_KEY, "123456789", "123456789")}
    response = requests.request("POST", url, headers=headers)
    return response



import sys
import requests
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "ZGUdjkFTWuuVFJYDUHoucR1Ry"
CONSUMER_SECRET = "xfFoq1ynIvsnZ7MeipWGT6XMFUx466i1tIaexUKXfqMmoj9EU1"
ACCESS_TOKEN = "1585874163280928769-ZUcNBBnMkW54p7yiUdZQDVT12JewfV"
TOKEN_SECRET = "VDbSxI4F0xylyupXJMwgU54UOfIbAZ2okFdjeoQ9x1Hdy"

def request_token():

    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri='oob')

    url = "https://api.twitter.com/oauth/request_token"

    try:
        response = oauth.fetch_request_token(url)
        resource_owner_oauth_token = response.get('oauth_token')
        resource_owner_oauth_token_secret = response.get('oauth_token_secret')
    except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(120)
    
    return resource_owner_oauth_token, resource_owner_oauth_token_secret

def get_user_authorization(resource_owner_oauth_token):

    authorization_url = f"https://api.twitter.com/oauth/authorize?oauth_token={resource_owner_oauth_token}"
    authorization_pin = input(f" \n Send the following URL to the user you want to generate access tokens for. \n → {authorization_url} \n This URL will allow the user to authorize your application and generate a PIN. \n Paste PIN here: ")

    return(authorization_pin)

def get_user_access_tokens(resource_owner_oauth_token, resource_owner_oauth_token_secret, authorization_pin):

    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=resource_owner_oauth_token, 
                            resource_owner_secret=resource_owner_oauth_token_secret, 
                            verifier=authorization_pin)
    
    url = "https://api.twitter.com/oauth/access_token"

    try: 
        response = oauth.fetch_access_token(url)
        access_token = response['oauth_token']
        access_token_secret = response['oauth_token_secret']
        user_id = response['user_id']
        screen_name = response['screen_name']
    except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(120)

    return(access_token, access_token_secret, user_id, screen_name)