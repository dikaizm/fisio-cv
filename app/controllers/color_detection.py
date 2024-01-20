import cv2 as cv
import numpy as np

class ColorDetection:
    def __init__(self, frame):
        self.frame = frame

    def set_frame(self, frame):
        self.frame = frame

    def detect_color(self):
        # Convert BGR to HSV
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

        # define range of red color in HSV
        lower_range = np.array([0, 50, 50])
        upper_range = np.array([10, 255, 255])

        mask = cv.inRange(hsv, lower_range, upper_range)
        res = cv.bitwise_and(self.frame, self.frame, mask=mask)
        
        return res, mask

    def find_contours(self, mask):
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        objects = []
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            objects.append((x, y, x + w, y + h))

        return objects

    def get_objects(self, frame):
        frame = self.set_frame(frame)
        _, mask = self.detect_color()
        objects = self.find_contours(mask)

        return objects