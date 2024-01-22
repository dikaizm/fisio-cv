import cv2 as cv
import numpy as np

from utils.camera import Frame
from utils.theme import Colors

class ColorDetection:
    def get_objects(self, frame):
        frame = cv.GaussianBlur(frame, (5, 5), 0)
        
        # Convert the frame from BGR to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # lower boundary GREEN color range values
        lower = np.array([35, 100, 60])
        upper = np.array([70, 255, 255])
        
        mask = cv.inRange(hsv, lower, upper)
        
        # Get only masked color
        # result = cv.bitwise_and(frame, frame, mask=mask)
        
        # Morphological operations
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, (5, 5))
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, (5, 5))
        
        # Find contours in the mask
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        return contours
    
    def get_keypoints(self, frame, contours):
        fr = Frame()
        colors = Colors()
        keypoints = []
            
        for i, contour in enumerate(contours, start=1):
            # Get the bounding box of the contour
            point_x, point_y, w, h = cv.boundingRect(contour)
            
            point = Point(point_x + w // 2, point_y + h // 2)

            keypoints.append(point)

            # Draw a rectangle around the detected object and label
            cv.rectangle(frame, (point_x, point_y), (point_x+w, point_y+h), colors.green, 2)
            fr.circle(frame, (point.x, point.y))
            fr.put_text(frame, str(i), (point.x + 10, point.y), color=colors.white)
        #endfor
        
        return keypoints
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y