import os
import dotenv
import requests

dotenv.load_dotenv()

def recent_search(word: str):
    """
        This function performs a recent search on Twitter using the Twitter API v2.
        It retrieves tweets that match the given word, phrase or query.
        Rate limits:
        - Free: 1 request per 15 minutes
        - Basic: 60 requests per 15 minutes
        - Pro: 300 requests per 15 minutes 
    """
    BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    if not BEARER_TOKEN:
        raise Exception("TWITTER_BEARER_TOKEN not found in environment variables")
    
    BASE_URL = "https://api.twitter.com/"

    url = BASE_URL + "2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }
    query_params = {
        "query": f"{word}",
        # "max_results": 1,
        "tweet.fields": "text,id",
    }
    
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")
    
    tweets = response.json().get("data", [])

    return tweets

def get_tweet_from_id(tweet_id: str):
    """
        This function retrieves a tweet by its ID using the Twitter API v2.
        It returns the tweet data in JSON format.
        Rate limits:
        - Free: 1 request per 15 minutes
        - Basic: 15 requests per 15 minutes
        - Pro: 900 requests per 15 minutes
    """
    BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    if not BEARER_TOKEN:
        raise Exception("TWITTER_BEARER_TOKEN not found in environment variables")
    
    BASE_URL = "https://api.twitter.com/"

    url = BASE_URL + f"2/tweets/{tweet_id}"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")
    
    tweet_data = response.json().get("data", {})    
    return tweet_data