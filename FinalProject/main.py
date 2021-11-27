#import
from imageai.Detection import ObjectDetection
import os
import cv2


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    model_path = "EnvFiles/yolo.h5"
    input_path = "input/1.jpeg"
    output_path = "output/out.jpg"

    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel(detection_speed="fast")
    detections = detector.detectObjectsFromImage(input_image=input_path,
    output_image_path=output_path)
    detectedObject = []

    image = cv2.imread(output_path)
    #Prints the detected objects
    for eachObject in detections:
        print(eachObject)
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        print(eachObject["box_points"])
        x= eachObject["box_points"][0]
        y= eachObject["box_points"][1]
        w=eachObject["box_points"][2]
        h=eachObject["box_points"][3]

        cv2.line(image, (x, y), (x, h), (0, 0, 255), 2)


    cv2.imshow("output", image)                         # Show image
    cv2.waitKey(0)                                      # Display the image infinitely until any keypress