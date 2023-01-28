import os
import requests
from dotenv import load_dotenv
load_dotenv()


BEARER_TOKEN = os.getenv('BEARER_TOKEN')
QUERY_SUFFIX = ' -filter:retweets filter:images'
API_URL = 'https://api.twitter.com/2/tweets/search/recent'


class Twitter():
    def __init__(self):
        self.client = None

    def search(self, query):
        images = []
        status = "OK"

        try:
            twitter_response = requests.get(API_URL, params={'query': query + QUERY_SUFFIX})

            if twitter_response.status_code == 200:
                for tweet in twitter_response.json()['data']:
                    if 'attachments' in tweet:
                        for attachment in tweet['attachments']['media_keys']:
                            images.append({'url': tweet['attachments']['media'][attachment]['url'], 'tweet': tweet['text']})
            elif twitter_response.status_code == 429:
                status = "Rate limit exceeded"
            elif twitter_response.status_code == 401:
                status = "Invalid Bearer Token"
            else:
                status = "Internal Server Error"
        except Exception:
            return {'images': [], 'status_code': 500, 'query': query, 'status_text': 'Internal Server Error'}

        return {'images': images, 'status_code': twitter_response.status_code, 'query': query, 'status_text': status}
