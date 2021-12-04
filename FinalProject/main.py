# import
from imageai.Detection import ObjectDetection
import os
import numpy as np
import cv2


IMAGE = False
VIDEO = True

# ---------------------------------------------------------------------
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
def detectFromVideo(input_path):
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

    vs = cv2.VideoCapture(input_path)  # open our video
    W = int(vs.get(3))
    H = int(vs.get(4))
    fps = vs.get(cv2.CAP_PROP_FPS)
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    cnt = 0;
    while True:
        cnt += 1
        # print("Frame number", cnt)
        try:
            (grabbed, image) = vs.read()
        except:
            break
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        if W is None or H is None:
            (H, W) = image.shape[:2]
        layerOutputs = net.forward(ln)

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > CONFIDENCE_THRESHOLD:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, YOLO actually returns the center (x, y)
                    # -coordinates of the bounding box followed by the boxes'
                    # width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
                                CONFIDENCE_THRESHOLD)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                # x = boxes[i][0]
                # y = boxes[i][1]
                # w = boxes[i][2]
                # h = boxes[i][3]
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[classIDs[i]]]

                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                print("{} detect! {},{},{},{}".format(LABELS[classIDs[i]], boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] +boxes[i][3]))
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

        # show the output image
        cv2.imshow("output", image)
        writer.write(image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()

    # release the file pointers
    print("[INFO] cleaning up...")
    writer.release()
    vs.release()


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    input_path = "input/1.jpeg"
    output_path = "output/out.jpg"
    video_input_path = "input/car.mp4"

    if IMAGE:
        detectFromImage(input_path, output_path)

    elif VIDEO:
        detectFromVideo(video_input_path)

    cv2.waitKey(0)  # Display the image infinitely until any keypress
