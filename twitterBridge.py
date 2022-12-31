import sys
import requests
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "ZGUdjkFTWuuVFJYDUHoucR1Ry"
CONSUMER_SECRET = "xfFoq1ynIvsnZ7MeipWGT6XMFUx466i1tIaexUKXfqMmoj9EU1"
ACCESS_TOKEN = "1585874163280928769-ZUcNBBnMkW54p7yiUdZQDVT12JewfV"
TOKEN_SECRET = "VDbSxI4F0xylyupXJMwgU54UOfIbAZ2okFdjeoQ9x1Hdy"

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