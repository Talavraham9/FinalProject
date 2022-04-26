from imageai.Detection import ObjectDetection
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np

execution_path = os.getcwd()

modelPath = "EnvFiles/yolo.h5"
inputPath = "input/1.jpeg"
outputPath = "output/newImage.jpg"

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, modelPath))
detector.loadModel(detection_speed="fast")

detections = detector.detectObjectsFromImage(input_image=inputPath, output_image_path=outputPath)

for eachObject in detections:
    # if eachObject["name"] == 'car' or eachObject["name"] == 'motorcycle' or eachObject["name"] == 'bench':
    print(eachObject["name"], " : ", eachObject["percentage_probability"])
