import os
import dotenv
import requests
from datetime import datetime
from django.utils.timezone import now as Now

from .models import Tweet

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
        "tweet.fields": "text,id,username,author_id,created_at",
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

def search_new_word(word: str) -> Tweet:
    """
        This function searches for a new word in the Twitter API and saves it to the database.
        It first checks if the word already exists in the database, if it does, it returns it.
        If it doesn't, it searches for it in the Twitter API and saves it to the database.
    """
    # Search for the word in the database
    # If it exists, return it
    if Tweet.objects.filter(target_word=word).exists():
        #TODO: Validate the tweet
        return Tweet.objects.get(target_word=word)
    
    # If it doesn't exist, search for it in the Twitter API
    tweets = recent_search(word)
    if not tweets:
        raise Exception(f"No tweets found for {word}")
    
    # Check if the tweet already exists in the database
    # There cannot be two target words with the same tweet id
    for tweet in tweets:
        if Tweet.objects.filter(tweet_id=tweet["id"]).exists():
            raise Exception(f"Tweet with id {tweet['id']} already exists in the database")
        
        word_position: int = tweet["text"].lower().index(word) if word in tweet["text"] else 0
        
        # Create a new tweet object and save it to the database
        tweet_obj = Tweet(
            target_word=word,
            target_word_position=word_position,
            last_checked_at=Now(),
            tweet_id=tweet["id"],
            username=tweet["username"],
            author_id=tweet["author_id"],
            tweet_text=tweet["text"],
            created_at=["created_at"],
        )
        tweet_obj.save()

        break

    return tweet_obj