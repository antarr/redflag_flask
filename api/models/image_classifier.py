from imageai.Classification import ImageClassification
import os
from pathlib import Path


class ImageClassifier():
    def __init__(self):
        self.classifier = ImageClassification()
        self.classifier.setModelTypeAsResNet50()
        self.classifier.setModelPath(os.path.join(os.getcwd(), "pretrained", "resnet50-19c8e357.pth"))
        self.classifier.loadModel()

    def classify(self, image_path):
        predictions, probabilities = self.classifier.classifyImage(image_path, result_count=5)
        classifations = []
        for index in range(len(predictions)):
            classifations.append({'prediction': predictions[index], 'probability': probabilities[index]})
        return classifations


# For testing purposes
if __name__ == '__main__':
    images_path = Path("images/")
    images = [str(path) for path in images_path.glob('*.jpg')]
    image_classifier = ImageClassifier()
    for image in images:
        print(image)
        classifictions = image_classifier.classify(image)
        print(classifictions)
        print('-----------------')
