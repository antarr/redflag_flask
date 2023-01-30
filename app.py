import os
from flask import Flask, request
from api.models.twitter import Twitter
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
TWITTER = Twitter()


@app.route('/search/<term>', methods=['GET'])
def search(term):
    response = TWITTER.search(term)
    return response, response['status_code']


@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_path)
        classifications = TWITTER.classify_image(full_path)
        return {'classifications': classifications, 'filename': filename}, 200
    return {'error': 'Invalid file type'}, 400


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
