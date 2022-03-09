# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt

IPHONE = True
ANDROID = False
RESIZE_VAL = 1
path = "input/distance_iphone.jpeg"
IPHONE_lower_bound  =np.array([0, 150, 140], np.uint8)
IPHONE_upper_bound = np.array([10, 255, 255], np.uint8)

ANDROID_lower_bound = np.array([160, 120, 120], np.uint8)
ANDROID_upper_bound = np.array([180, 255, 255], np.uint8)


# ---------------------------------------------------------------------
# function      : draw_rect
# Description   : Gets a contour and draws on the picture rectangles according to the contours
# ---------------------------------------------------------------------
def draw_rect(contour):
    img_copy = np.copy(img)
    height, width, channel = img.shape
    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        if ( x > width // 2):
            cv2.circle(img_copy, (x, y+h), radius=4, color=(0, 255,0 ), thickness=-1)
        elif (x < width // 2):
            cv2.circle(img_copy, (x+w, y+h), radius=4, color=(0, 255,0 ), thickness=-1)




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
    if IPHONE:
        lower_bound = IPHONE_lower_bound
        upper_bound = IPHONE_upper_bound
    elif ANDROID:
        lower_bound = ANDROID_lower_bound
        upper_bound = ANDROID_upper_bound

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