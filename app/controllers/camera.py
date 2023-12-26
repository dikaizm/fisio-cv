import cv2 as cv
import math
import numpy as np

class Camera:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        
    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self):
        self.cap.release()
        cv.destroyAllWindows()


class Frame:
    def __init__(self, frame):
        self.frame = frame
        self.height, self.width, self.channels = frame.shape
    
    def add_meta_info(self, frame, text, font, color, position):
        w, h = self.height, self.width
        text_size = cv.getTextSize(text, font, 1, 2)[0]
        text_position = (w - text_size[0] - position[0], h - text_size[1] + position[1])

        cv.putText(frame, text, text_position, font, 1, color, 2, cv.LINE_AA)

    def draw_angle_indicator(self, frame, center, radius, start_angle, end_angle, color):
        # Convert angles to radians
        start_angle_rad = math.radians(start_angle)
        end_angle_rad = math.radians(end_angle)

        # Calculate start and end points of the arc
        start_point = (
            int(center[0] + radius * np.cos(start_angle_rad)),
            int(center[1] + radius * np.sin(start_angle_rad))
        )
        end_point = (
            int(center[0] + radius * np.cos(end_angle_rad)),
            int(center[1] + radius * np.sin(end_angle_rad))
        )

        # Draw the arc on the frame
        cv.ellipse(frame, center, (radius, radius), 0, start_angle - 180, end_angle - 180, color, 2)

        # Draw lines connecting the center to the start and end points
        cv.line(frame, center, start_point, color, 2)
        cv.line(frame, center, end_point, color, 2)