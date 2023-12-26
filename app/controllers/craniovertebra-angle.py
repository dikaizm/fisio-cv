import cv2 as cv
import mediapipe as mp
import math
import numpy as np

class CraniovertebraAngle:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_style = mp.solutions.drawing_styles

    def find_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_angle(self, x1, y1, x2, y2, facing):
        theta = math.atan2(y2 - y1, x2 - x1)
        degree = int(math.degrees(theta))

        if facing == "left":
            degree += 180
        else:
            degree *= -1

        return degree
    
    def find_midpoint(self, x1, y1, x2, y2):
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))
    
    def get_landmarks(self, frame):
        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.pose.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        return results.pose_landmarks