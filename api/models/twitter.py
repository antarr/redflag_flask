import os
import requests
from dotenv import load_dotenv
load_dotenv()


class Twitter():
    def __init__(self):
        self.client = None
        self.BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
        self.QUERY_SUFFIX = ' -filter:retweets filter:images'
        self.API_URL = 'https://api.twitter.com/2/tweets/search/recent'

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.BEARER_TOKEN}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def search(self, query):
        images = []
        status = "OK"
        expansions = 'attachments.media_keys'
        media_fields = 'url,preview_image_url,variants,alt_text'
        max_results = 100
        json_response = requests.get(self.API_URL,
                                     auth=self.bearer_oauth,
                                     params={'query': query + ' has:images',
                                             'tweet.fields': 'author_id,attachments',
                                             'expansions': expansions,
                                             'media.fields': media_fields,
                                             'max_results': max_results})

        if json_response.status_code == 200:
            for media in json_response.json()['includes']:
                for image in json_response.json()['includes'][media]:
                    images.append({'url': image['url'], 'key': image['media_key']})
        elif json_response.status_code == 429:  # rate limit exceeded
            status = "Rate limit exceeded"  # set status to rate limit exceeded

        elif json_response.status_code == 401:  # invalid bearer token
            status = "Invalid Bearer Token"  # set status to invalid bearer token
        else:   # all other errors
            print(json_response.text)
            status = "Internal Server Error"   # set status to internal server error

        return {'images': images, 'status_code': json_response.status_code, 'query': query, 'status_text': status}
