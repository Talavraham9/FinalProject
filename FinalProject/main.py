# import
import os
import numpy as np
import cv2

IMAGE = True
VIDEO = False
CAMERA = False


# # -------------------------------------------------------------------
# function      : detect
# Description   : The function receives an image and returns an image
#                 with rectangles on the objects
# ---------------------------------------------------------------------
def detect(img):
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
        print("{} detect".format(LABELS[class_ids[i]]))
        cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img


# # -------------------------------------------------------------------
# function      : detectFromImage
# Description   : Detection objects from an image
# ---------------------------------------------------------------------
def detectFromImage(input_path, output_path):
    img = cv2.imread(input_path)  # open camera
    img = detect(img)

    # Saving the image
    cv2.imwrite(output_path, img)
    cv2.imshow("output", img)  # show the output image


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
    input_video_path = "input/motorcycle.mp4"
    output_video_path = 'output/videoOutput.mp4'

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    LABELS_FILE = 'C:/darknet-master/data/coco.names'
    CONFIG_FILE = 'C:/darknet-master/cfg/yolov3-tiny.cfg'
    WEIGHTS_FILE = 'EnvFiles/yolov3-tiny.weights'
    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
    CONFIDENCE_THRESHOLD = 0.5
    LABELS = open(LABELS_FILE).read().strip().split("\n")
    np.random.seed(4)  # makes the random numbers predictable
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")  # Colors of the objects

    if IMAGE:
        detectFromImage(input_image_path, output_image_path)

    elif VIDEO or CAMERA:
        detectFromVideo(input_video_path, output_video_path)

    cv2.waitKey(0)  # Display the image infinitely until any keypress
