# import
from imageai.Detection import ObjectDetection
import os
import numpy as np
import cv2

IMAGE = False
VIDEO = True
CAMERA = True
# # ---------------------------------------------------------------------
# function      : detectFromImage
# Description   : Detection objects from an image
# ---------------------------------------------------------------------
def detectFromImage(input_path, output_path):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("EnvFiles/yolo.h5")
    detector.loadModel(detection_speed="fast")
    detections = detector.detectObjectsFromImage(input_image=input_path,
                                                 output_image_path=output_path)
    image = cv2.imread(output_path)

    # Prints the detected objects
    for eachObject in detections:
        print(eachObject)
        print(eachObject["name"], " : ", eachObject["percentage_probability"])
        print(eachObject["box_points"])
        x = eachObject["box_points"][0]
        y = eachObject["box_points"][1]
        w = eachObject["box_points"][2]
        h = eachObject["box_points"][3]

        cv2.line(image, (x, y), (x, h), (0, 0, 255), 2)

    # Show result image
    cv2.imshow("output", image)


# ---------------------------------------------------------------------
# function      : detectFromVideo
# Description   : Detection objects from a video
# ---------------------------------------------------------------------
def detectFromVideo():
    INPUT_FILE = "input/car.mp4"
    OUTPUT_FILE = 'output/videoDetections.avi'
    LABELS_FILE = 'C:/darknet-master/data/coco.names'
    CONFIG_FILE = 'C:/darknet-master/cfg/yolov3.cfg'
    WEIGHTS_FILE = 'EnvFiles/yolov3.weights'
    CONFIDENCE_THRESHOLD = 0.7
    LABELS = open(LABELS_FILE).read().strip().split("\n")

    # Output video
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(OUTPUT_FILE, fourcc, 30, (800, 600), True)

    np.random.seed(4)  # makes the random numbers predictable
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # Colors of the objects
    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
    if CAMERA:
        cap = cv2.VideoCapture((0 + cv2.CAP_DSHOW))  # open camera
    elif VIDEO:
        cap = cv2.VideoCapture(INPUT_FILE)  # open our video

    while True:
        ret, img = cap.read()
        height, weight, _ = img.shape
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
                    centre_x = int(detection[0] * weight)
                    centre_y = int(detection[1] * height)
                    w = int(detection[2] * weight)
                    h = int(detection[3] * height)

                    x = int(centre_x - w / 2)
                    y = int(centre_y - h / 2)

                    box.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = np.array(cv2.dnn.NMSBoxes(box, confidences, 0.5, 0.4))
        # ensure at least one detection exists
        for i in indexes.flatten():
            x, y, w, h = box[i]
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.2f}".format(LABELS[class_ids[i]], confidences[i])
            cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("output", img)  # show the output image
        writer.write(img)
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
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    input_path = "input/1.jpeg"
    output_path = "output/out.jpg"


    if IMAGE:
        detectFromImage(input_path, output_path)

    elif VIDEO or CAMERA:
        detectFromVideo()

    cv2.waitKey(0)  # Display the image infinitely until any keypress
