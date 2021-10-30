from imageai.Detection import ObjectDetection
import os
import tensorflow as tf
import numpy as np

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path, "EnvFiles/yolo.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="1.jpeg",
output_image_path="newimage.jpg")
labelsPath = os.path.sep.join(["coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    print(eachObject["box_points"])
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
