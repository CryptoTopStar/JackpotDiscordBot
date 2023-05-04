import sys
import requests
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "6zlIblJS3RkYw4AdgRgd9okss"
CONSUMER_SECRET = "rCa1whfWUoKAQr5ReoOmYt1mKmjRPJvRDFMfZE9fwADGr75Xeu"
ACCESS_TOKEN = "1585874163280928769-ZUcNBBnMkW54p7yiUdZQDVT12JewfV"
TOKEN_SECRET = "rCa1whfWUoKAQr5ReoOmYt1mKmjRPJvRDFMfZE9fwADGr75Xeu"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAEhsnAEAAAAAwp4XBmyb1A42S8%2Fcq7XR7ePGsWQ%3Df1Hibmi8ExOhG6W03yN02RCuziXTAuSMaaUnj0eZInaHRUW6VY"

def link():
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri='oob')
    url = "https://api.twitter.com/oauth/request_token"
    try:
        response = oauth.fetch_request_token(url)
        resource_owner_oauth_token = response.get('oauth_token')
        resource_owner_oauth_token_secret = response.get('oauth_token_secret')
    except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(120)

    authorization_url = f"https://api.twitter.com/oauth/authorize?oauth_token={resource_owner_oauth_token}"

    return authorization_url, resource_owner_oauth_token, resource_owner_oauth_token_secret

def auth(resource_owner_oauth_token, resource_owner_oauth_token_secret, authorization_pin):

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
    except:
        return None

    return [access_token, access_token_secret, user_id, screen_name]

## given a user access_tokem, access_token_secret, user_id, screen_name
## and a tweet id, return if the user has liked the tweet
def likedRetweeted(access_token, access_token_secret, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/lookup.json?id={tweet_id}&include_entities=true"
    try:
        response = oauth.get(url)
        try:
            hasRetweet = response.json()[0]['retweeted']
        except:
            hasRetweet = False
            
        try:
            hasLike = response.json()[0]['favorited']
        except:
            hasLike = False
        return hasLike, hasRetweet
    except:
        return False, False
    
## see if the last 10 tweets user has posted is a comment on the tweet from tweet_id
def hasCommented(access_token, access_token_secret, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?count=15"
    try:
        response = oauth.get(url)
        for tweet in response.json():
            if tweet['in_reply_to_status_id_str'] == tweet_id:
                return True
        return False
    except:
        return False
    
## see if tweet_id_original is a comment on tweet_id
def isComment(access_token, access_token_secret, tweet_id_original, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/show.json?id={tweet_id}"
    try:
        response = oauth.get(url)
        if response.json()['in_reply_to_status_id_str'] == tweet_id_original:
            return True
        return False
    except:
        return False
    
## get the link of their last tweet
def getLastTweetLink(access_token, access_token_secret):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?count=1"
    try:
        response = oauth.get(url)
        return response.json()[0]['entities']['urls'][0]['expanded_url']
    except:
        return None