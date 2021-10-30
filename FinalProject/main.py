from imageai.Detection import ObjectDetection
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path, "EnvFiles/yolo.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="photos/img.jpeg",
output_image_path="photosNew/imagenew.jpg")

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )