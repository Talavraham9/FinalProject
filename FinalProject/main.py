from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path, "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="C:/Users/MOEUser/Desktop/final project/yolov5-master/images/1.jpeg",
output_image_path="C:/Users/MOEUser/PycharmProjects/pythonProject/imagenew.jpg")

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )