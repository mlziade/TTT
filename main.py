import os
import dotenv
import requests

# Load environment variables
dotenv.load_dotenv()

# Requires Pro plans
# Pro rate-limiting: 300 requests per 15 minutes
def full_archive_search(word: str):
    BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    if not BEARER_TOKEN:
        raise Exception("TWITTER_BEARER_TOKEN not found in environment variables")
    
    BASE_URL = "https://api.twitter.com/"

    url = BASE_URL + "2/tweets/search/all"
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
    return response.json()

# Free rate-limiting: 1 request per 15 minutes
# Basic rate-limiting: 5 requests per 15 minutes
# Pro rate-limiting: 300 requests per 15 minutes
def recent_search(word: str):
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
    return response.json()

def main():
    # print(full_archive_search("python"))
    print(recent_search("python"))


if __name__ == "__main__":
    main()