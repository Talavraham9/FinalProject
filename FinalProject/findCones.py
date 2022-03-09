# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt

RESIZE_VAL = 1
path = "input/distance_android.jpeg"


def draw_rect(contour):
    img_copy = np.copy(img)
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img_copy, (x, y + h), (x + w, y), (255, 255, 255), 2)
    return img_copy

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == '__main__':
    # load the image
    image = cv2.imread(path)
    height, width, channel= image.shape
    img = cv2.resize(image, (width // RESIZE_VAL, height // RESIZE_VAL), interpolation=cv2.INTER_AREA)

    # convert to hsv colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower bound and upper bound for Green color
    lower_bound = np.array([160, 100, 100],np.uint8)
    upper_bound = np.array([180, 255, 255],np.uint8)

    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    #define kernel size
    kernel = np.ones((7,7),np.uint8)

    # Remove unnecessary noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Segment only the detected region
    segmented_img = cv2.bitwise_and(img, img, mask=mask)

    # Find contours from the mask
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = draw_rect(contours)

    #Show images
    cv2.imshow("rect", rect)
    cv2.imwrite("output/distance_android_rec.jpeg", rect)

    cv2.waitKey(0)
    cv2.destroyAllWindows()