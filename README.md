# Image Crawler and ML Analysis App
This is a Flask app that allows you to search for images on a social network and get ML analysis of them. It has two endpoints: 

1. Search via crawler by keyword on a social network and return ML analysis
2. Upload images directly and get ML analysis for that image

## Prerequisites
- Python 3.11
- Pip 
- Twitter API keys

## Installation
1. Install Python 3.11 and pip:
```
2. Install Flask and other dependencies:
```
pip install Flask
pip install <any other ML library>
pip install <any other social network API>
```
3. Clone the repository:
```
git clone https://github.com/<your_username>/image-crawler-ml-analysis.git
```
4. Navigate to the cloned directory and run the app:
```
cd image-crawler-ml-analysis
flask --app api/app.py run
```

## Usage
1. To search via crawler by keyword on a social network and return ML analysis, use the following endpoint:
```
POST http://localhost:5000/search
```
The request body should contain the keyword to search for. The response will be a JSON containing up to 5 images and their ML analysis. 

2. To upload images directly and get ML analysis for that image, use the following endpoint:
```
POST http://localhost:5000/analyze
```
The request body should contain the image file to be analyzed. The response will be a JSON containing the ML analysis of the image. 

## Credits
This app is developed by [Antarr](https://antarr.dev/).