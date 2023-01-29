import os
import requests
from dotenv import load_dotenv

from api.models.image_classifier import ImageClassifier
load_dotenv()


class Twitter():
    def __init__(self):
        self.client = None
        self.BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
        self.API_URL = 'https://api.twitter.com/2/tweets/search/recent'
        self.IMAGE_CLASSIFIER = ImageClassifier()

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
        max_results = 25
        json_response = requests.get(self.API_URL,
                                     auth=self.bearer_oauth,
                                     params={'query': query + ' has:images',
                                             'tweet.fields': 'author_id,attachments',
                                             'expansions': expansions,
                                             'media.fields': media_fields,
                                             'max_results': max_results})

        if json_response.status_code == 200:  # success
            if 'includes' in json_response.json():
                for media in json_response.json()['includes']:
                    for count, image in enumerate(json_response.json()['includes'][media]):
                        if count >= 5:
                            break
                        local_path = self.save_image_to_tmp(image['url'])
                        image_classes = self.classify_image(local_path)
                        images.append({'url': image['url'], 'key': image['media_key'], 'classifications': image_classes})
        elif json_response.status_code == 429:  # rate limit exceeded
            status = "Rate limit exceeded"  # set status to rate limit exceeded

        elif json_response.status_code == 401:  # invalid bearer token
            status = "Invalid Bearer Token"  # set status to invalid bearer token
        else:   # all other errors
            print(json_response.text)
            status = "Internal Server Error"   # set status to internal server error

        return {'images': images, 'status_code': json_response.status_code, 'query': query, 'status_text': status}

    def save_image_to_tmp(self, image_url):
        image_path = f'/tmp/{image_url.split("/")[-1]}'
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)
        return image_path

    def classify_image(self, image_path):
        return self.IMAGE_CLASSIFIER.classify(image_path)
