# import
import os

import PIL.Image
import numpy as np
import cv2
from shapely.geometry import Polygon
from shapely import geometry
import flask
from flask import Flask, json, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/recieve_image",methods=["POST"])
def post_img():
    if request.method == "POST":
        data = request.files.get("image")
        img = PIL.Image.open(data)
        img = img.rotate(270)
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        object, severity = detect(opencvImage)
        img.show()

    response = flask.jsonify({'sever': severity, "obj": object})
    return response



# define
IMAGE = True
VIDEO = False
CAMERA = False
RED_COLOR = (0, 0, 255)
ORANGE_COLOR = (0, 165, 255)
YELLOW_COLOR = (51, 255, 255)
# Points of the red, orange, yellow polygons
redPoly = [[-0.16493055555555555, 1.048828125],
           [0.1605902777777778, 0.70263671875],
           [0.8472222222222222, 0.71044921875],
           [1.1302083333333333, 1.0732421875]]
orangePoly = [[0.1605902777777778 ,0.70263671875],
              [0.3888888888888889 ,0.498046875],
              [0.6796875, 0.49951171875],
              [0.8472222222222222 ,0.71044921875]]
yellowPoly = [[0.3888888888888889, 0.498046875],
              [0.4626736111111111, 0.4287109375],
              [0.6284722222222222, 0.4296875],
              [0.6796875 ,0.49951171875]]


# -------------------------------------------------------------------
# function      : inPoly
# Description   : return true/false if object in polygon
# ---------------------------------------------------------------------
def inPoly(x, y, w, h, img):
    # Draw polygon on image
    cv2.polylines(img, [np.array([redPoly], np.int32)], True, RED_COLOR, 9)
    cv2.polylines(img, [np.array([orangePoly], np.int32)], True, ORANGE_COLOR, 9)
    cv2.polylines(img, [np.array([yellowPoly], np.int32)], True, YELLOW_COLOR, 9)

    cv2.fillPoly(img, [np.array([redPoly], np.int32)],RED_COLOR)
    cv2.fillPoly(img, [np.array([orangePoly], np.int32)], ORANGE_COLOR)
    cv2.fillPoly(img, [np.array([yellowPoly], np.int32)], YELLOW_COLOR)

    # Creates a polygon of the identified object
    polygonDetect = Polygon([(x + w, y + h), (x, y + h), (x, y), (x + w, y)])

    # Create a shapely Polygon from a list
    polyRed = geometry.Polygon([[p[0], p[1]] for p in redPoly])
    polyOrange = geometry.Polygon([[p[0], p[1]] for p in orangePoly])
    polyYellow = geometry.Polygon([[p[0], p[1]] for p in yellowPoly])

    if (polyRed.intersection(polygonDetect)):  # Checks if object in red poly
        print("The object is inside the RED polygon")
        return 3
    else:
        if (polyOrange.intersection(polygonDetect)):  # Checks if object in orange poly
            print("The object is inside the ORANGE polygon")
            return 2
        else:
            if (polyYellow.intersection(polygonDetect)):  # Checks if object in yellow poly
                print("The object is inside the YELLOW polygon")
                return 1
            else:  # The object is outside
                print("The object is outside the polygons")
                return 0


# -------------------------------------------------------------------
# function      : detect
# Description   : The function receives an image and returns an image
#                 with rectangles on the objects
# ---------------------------------------------------------------------
def detect(img):
    global doOnce
    height, width, _ = img.shape
    # Finds the polygon according to the proportion of the image
    if doOnce == False:
        doOnce = True
        for i in range(len(redPoly)):
            redPoly[i][0] = redPoly[i][0] * width
            redPoly[i][1] = redPoly[i][1] * height
        for i in range(len(orangePoly)):
            orangePoly[i][0] = orangePoly[i][0] * width
            orangePoly[i][1] = orangePoly[i][1] * height
        for i in range(len(yellowPoly)):
            yellowPoly[i][0] = yellowPoly[i][0] * width
            yellowPoly[i][1] = yellowPoly[i][1] * height

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)

    output = net.getUnconnectedOutLayersNames()
    layers = net.forward(output)

    box = []
    confidences = []
    class_ids = []

    for out in layers:  # loop over each of the layer outputs
        for detection in out:  # loop over each of the detections
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE_THRESHOLD:
                centre_x = int(detection[0] * width)
                centre_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(centre_x - w / 2)
                y = int(centre_y - h / 2)

                box.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = np.array(cv2.dnn.NMSBoxes(box, confidences, 0.5, 0.4))
    object ="NONE"
    severity= 0
    # ensure at least one detection exists
    for i in indexes.flatten():
        x, y, w, h = box[i]
        currSeverity=inPoly(x, y, w, h, img)
        if currSeverity != 0 and currSeverity > severity:
            severity = currSeverity
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.2f}".format(LABELS[class_ids[i]], confidences[i])
            print("{} detect".format(LABELS[class_ids[i]]))
            object = LABELS[class_ids[i]]
            cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.imshow("output", img)  # show the output image

    return object,severity



# ---------------------------------------------------------------------
# function      : detectFromVideo
# Description   : Detection objects from a video
# ---------------------------------------------------------------------
def detectFromVideo(input_video_path, output_video_path):
    if CAMERA:
        cap = cv2.VideoCapture((0 + cv2.CAP_DSHOW))  # open camera
    elif VIDEO:
        cap = cv2.VideoCapture(input_video_path)  # open our video

    # Output video
    writer = cv2.VideoWriter(output_video_path, -1, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, img = cap.read()
        if ret:
            img = detect(img)
        else:
            exit(1)
        cv2.imshow("output", img)  # show the output image
        writer.write(img)  # save output

        if cv2.waitKey(1) & 0xff == ord("q"):
            break

    # release the file pointers
    print("[INFO] cleaning up...")
    writer.release()
    cap.release()
    cv2.destroyAllWindows()


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == '__main__':
    input_image_path = "input/car.jpeg"
    output_image_path = "output/out.jpg"
    input_video_path = "input/car3.mp4"
    output_video_path = 'output/videoOutputTiny.mp4'

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    LABELS_FILE = 'C:/darknet-master/data/coco.names'
    CONFIG_FILE = 'C:/darknet-master/cfg/yolov3-tiny_obj.cfg'
    WEIGHTS_FILE = 'EnvFiles/yolov3-tiny.weights'
    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
    CONFIDENCE_THRESHOLD = 0.5
    LABELS = open(LABELS_FILE).read().strip().split("\n")
    np.random.seed(4)  # makes the random numbers predictable
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # Colors of the objects
    doOnce = False

    app.run(host='192.168.1.114', port=5000)

    # if IMAGE:
    #     detect(input_image_path)
    #
    # elif VIDEO or CAMERA:
    #     detectFromVideo(input_video_path)
    #
    # cv2.waitKey(0)  # Display the image infinitely until any keypress
