from logging import error
import os
import requests
import json
import tweepy
from datetime import date
from dotenv import load_dotenv

#loads api keys and other environmentals
load_dotenv()

#set url to fetch getTop from.
url = "http://yacker.co:4000/graphql"

#graphql query
query = """
{
  getTop{
    school
    id
    content
  }
}
"""

#env vars set
bearerToken       = os.getenv("BEARER_TOKEN")
accessToken       = os.getenv("ACCESS_TOKEN")
accessTokenSecret = os.getenv("ACCESS_TOKEN_SECRET")
apiKeySecret      = os.getenv("API_KEY_SECRET")
apiKey            = os.getenv("API_KEY")

#authorization from tweepy
auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken, accessTokenSecret)

#tweepy api object
api = tweepy.API(auth)

#verify credentials
try:
    api.verify_credentials()
    print("Everything works")
except:
    print("Nothing works")

#get today's date.
today = str(date.today())

#get request to grapqhl endpoint.
r = requests.get(url, json={'query': query})

#load response json object as python dict
payload = json.loads(r.text)

#load items from dictionary to python variables
topSchool  = payload['data']['getTop'][0]['school']
topID      = payload['data']['getTop'][0]['id']
topContent = payload['data']['getTop'][0]['content']

#limit content to 150 chars
info = topContent[:150] + (topContent[150:] and '...')

#format status
post = {
    "status": "Top post of " + today + ":\n\"" + info + "\" #" +topSchool + "\n" + 
    "www.yacker.co/" + topSchool + "/" + topID 
}

status = post["status"]
#post status to twitter.
api.update_status(status)