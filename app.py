from flask import Flask
from api.models.twitter import Twitter


app = Flask(__name__)
TWITTER = Twitter()


@app.route('/search/<term>')
def search(term):
    response = TWITTER.search(term)
    return response


if __name__ == '__main__':
    app.run()
