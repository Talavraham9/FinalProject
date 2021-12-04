#import
from imageai.Detection import ObjectDetection
import os
import cv2
import cv2 as cv
import numpy as np
from imageai.Detection import VideoObjectDetection
# from shapely.geometry import Point, Polygon
from matplotlib import pyplot as plt


IMAGE = True
VIDEO = False

# ---------------------------------------------------------------------
# function      : inputFromImage
# Description   : Detection objects from an image, for each object prints
#                 the details on it At the end shows the image with the detections
# ---------------------------------------------------------------------
def inputFromImage(input_path,output_path, detector):
    execution_path = os.getcwd() + "/output"
    detections = detector.detectObjectsFromImage(input_image=input_path,
    output_image_path=output_path)
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

    # Show result image
    cv2.imshow("output", image)

# ---------------------------------------------------------------------
# function      : detectFromVideo
# Description   : Detection objects from a video, For each frame, a second
#                 and a minute prints the detection, and save new video
#                 with the detections
# ---------------------------------------------------------------------
def detectFromVideo(input_path, detector):
    execution_path = os.getcwd()+"/output"

    def forFrame(frame_number, output_array, output_count):
        print("FOR FRAME ", frame_number)
        print("Output for each object : ", output_array)
        print("Output count for unique objects : ", output_count)
        print("------------END OF A FRAME --------------")

    def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
        print("SECOND : ", second_number)
        print("Array for the outputs of each frame ", output_arrays)
        print("Array for output count for unique objects in each frame : ", count_arrays)
        print("Output average count for unique objects in the last second: ", average_output_count)
        print("------------END OF A SECOND --------------")

    def forMinute(minute_number, output_arrays, count_arrays, average_output_count):
        print("MINUTE : ", minute_number)
        print("Array for the outputs of each frame ", output_arrays)
        print("Array for output count for unique objects in each frame : ", count_arrays)
        print("Output average count for unique objects in the last minute: ", average_output_count)
        print("------------END OF A MINUTE --------------")

    detections = detector.detectObjectsFromVideo(
        input_file_path=os.path.join(input_path),
        output_file_path=os.path.join(execution_path, "videoDetections"),
        frames_per_second=20,
        per_second_function=forSeconds,
        per_frame_function=forFrame,
        per_minute_function=forMinute,
        minimum_percentage_probability=40,
        detection_timeout=120
    )

    #Prints the detected objects
    for eachObject in detections:
        print(eachObject)
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        print(eachObject["box_points"])
        x= eachObject["box_points"][0]
        y= eachObject["box_points"][1]
        w=eachObject["box_points"][2]
        h=eachObject["box_points"][3]



# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    model_path = "EnvFiles/yolo.h5"
    input_path = "input/1.jpeg"
    output_path = "output/out.jpg"
    video_input_path = "input/car.mp4"


    if IMAGE:
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(model_path)
        detector.loadModel(detection_speed="fast")

        inputFromImage(input_path,output_path, detector)

    elif VIDEO:
        detector = VideoObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(model_path)
        detector.loadModel(detection_speed="flash")

        detectFromVideo(video_input_path, detector)

    cv2.waitKey(0)                                      # Display the image infinitely until any keypress