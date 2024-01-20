from datetime import datetime
import time
import cv2 as cv
import mediapipe as mp
import math

import numpy as np
from app.controllers.color_detection import ColorDetection
from controllers.camera import Camera, Frame

class ForwardShoulderAngle:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_style = mp.solutions.drawing_styles
        self.results = []

    def find_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_distance_x(self, x1, x2):
        return math.sqrt((x2 - x1)**2)
    
    def find_angle(self, x1, y1, x2, y2, facing = None):
        theta = math.acos( (y2 -y1)*(-y1) / (math.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
        degree = int(180/math.pi)*theta

        return degree
    
    def get_keypoints(self, objects, w, h):
        # object with higher position to lower
        objects = sorted(objects, key=lambda x: x[1], reverse=True)
        tragus = objects[0]
        c7 = objects[1]
        humerus = objects[2]
        
        keypoints = {}
        # Tragus
        keypoints["tragus_x"] = tragus.x
        keypoints["tragus_y"] = tragus.y
        # C7
        keypoints["c7_x"] = c7.x
        keypoints["c7_y"] = c7.y
        # Humerus
        keypoints["humerus_x"] = humerus.x
        keypoints["humerus_y"] = humerus.y
        
        return keypoints
    
    def get_angle(self, frame, keypoints, w, h, font, colors):
        l_shldr_x, l_shldr_y = keypoints["l_shldr_x"], keypoints["l_shldr_y"]
        r_shldr_x, r_shldr_y = keypoints["r_shldr_x"], keypoints["r_shldr_y"]
        l_ear_x, l_ear_y = keypoints["l_ear_x"], keypoints["l_ear_y"]
        r_ear_x, r_ear_y = keypoints["r_ear_x"], keypoints["r_ear_y"]
        l_eye_x, l_eye_y = keypoints["l_eye_x"], keypoints["l_eye_y"]
        r_eye_x, r_eye_y = keypoints["r_eye_x"], keypoints["r_eye_y"]
        nose_x = keypoints["nose_x"]
        
        green = colors["green"]
        red = colors["red"]
        yellow = colors["yellow"]
        pink = colors["pink"]
        
        # Calculate distance between left shoulder and right shoulder points.
        offset_shldr = self.find_distance_x(l_shldr_x, r_shldr_x)
        
        # Assist to align the camera to point at the side view of the person.
        if offset_shldr < 50:
            cv.putText(frame, 'Aligned', (10, h -50), font, 0.9, green, 2)
        else:
            cv.putText(frame, 'Not Aligned', (10, h -50), font, 0.9, red, 2)
        
        # Get midpoint of left and right shoulder points.
        mx, my = self.find_midpoint(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        
        cv.line(frame, (l_shldr_x, l_shldr_y), (r_shldr_x, r_shldr_y), yellow, 2)

        # Determine whether the person is facing left or right.
        if mx > nose_x:
            facing = 'left'
        else:
            facing = 'right'
            
        cv.putText(frame, 'Facing: ' + facing, (10, h - 20), font, 0.9, green, 2)

        # Get tragus
        if facing == 'left':
            l_eye_to_ear = self.find_distance(l_eye_x, l_eye_y, l_ear_x, l_ear_y)
            trg_x, trg_y = int(l_ear_x + (l_eye_to_ear / 2)), int(l_ear_y - (l_eye_to_ear / 6))
        else:
            r_eye_to_ear = self.find_distance(r_eye_x, r_eye_y, r_ear_x, r_ear_y)
            trg_x, trg_y = int(r_ear_x - (r_eye_to_ear / 2)), int(r_ear_y - (r_eye_to_ear / 6))

        cv.circle(frame, (trg_x, trg_y), 7, pink, -1)

        # Calculate distance between tragus and midpoint.
        trg_to_mid = self.find_distance(trg_x, trg_y, mx, my)
        neck_ratio = 0.25
        if facing == 'left':
            c7_x, c7_y = int(mx + (trg_to_mid * neck_ratio)), int(my - (trg_to_mid * neck_ratio))
        else:
            c7_x, c7_y = int(mx - (trg_to_mid * neck_ratio)), int(my - (trg_to_mid * neck_ratio))
        
        cv.circle(frame, (c7_x, c7_y), 7, pink, -1)
        cv.circle(frame, (mx, my), 7, yellow, -1)
        
        # Connect shoulder to c7 point
        cv.line(frame, (l_shldr_x, l_shldr_y), (c7_x, c7_y), yellow, 2)
        cv.line(frame, (r_shldr_x, r_shldr_y), (c7_x, c7_y), yellow, 2)
        
        # Connect tragus to c7 point
        cv.line(frame, (trg_x, trg_y), (c7_x, c7_y), yellow, 2)
        
        # Draw imaginary horizontal line from c7.
        cv.line(frame, (c7_x - 50, c7_y), (c7_x + 50, c7_y), yellow, 2)
        
        # Draw imaginary vertical line from c7.
        cv.line(frame, (c7_x, c7_y - 200), (c7_x, c7_y + 200), yellow, 2)
        cv.circle(frame, (c7_x, c7_y - 200), 7, yellow, -1)
        cv.circle(frame, (c7_x, c7_y + 200), 7, yellow, -1)

        # Draw landmarks.
        cv.circle(frame, (l_shldr_x, l_shldr_y), 7, green, -1)

        # cv.circle(frame, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
        cv.circle(frame, (r_shldr_x, r_shldr_y), 7, red, -1)

        # The threshold angles to determine posture condition
        if facing == 'left':
            shldr_x, shldr_y = l_shldr_x, l_shldr_y
            text_pos = (c7_x + 30, c7_y + 40)
        else:
            shldr_x, shldr_y = r_shldr_x, r_shldr_y
            text_pos = (c7_x - 50, c7_y + 40)
                
        # Calculate shoulder angle
        shoulder_angle = self.find_angle(shldr_x, shldr_y, c7_x, c7_y)
    
        # Save results
        self.results.append((int(shoulder_angle), datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))        
    
        # Text string for display.
        shoulder_angle_text = 'Shoulder angle: ' + str(int(shoulder_angle))
        
        if shoulder_angle >= 0 and shoulder_angle <= 22:
            cv.putText(frame, shoulder_angle_text, (10, 30), font, 0.9, green, 2)
            cv.putText(frame, str(int(shoulder_angle)), text_pos, font, 0.9, green, 2)

            # Join landmarks.
            cv.line(frame, (shldr_x, shldr_y), (c7_x, c7_y), green, 4)

        else:
            cv.putText(frame, shoulder_angle_text, (10, 30), font, 0.9, red, 2)
            cv.putText(frame, str(int(shoulder_angle)), text_pos, font, 0.9, red, 2)

            # Join landmarks.
            cv.line(frame, (shldr_x, shldr_y), (c7_x, c7_y), red, 4)
    
    
    def run(self):
        camera = Camera()
        camera.is_opened()
        
        while True:
            ret, frame = camera.get_frame()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            
            fr = Frame(frame)
            frame = fr.frame
            
            objects = ColorDetection().get_objects(frame)
            keypoints = self.get_keypoints(objects, fr.width, fr.height)
            if keypoints:
                self.get_angle(frame, keypoints, fr.width, fr.height, fr.font, fr.colors)
                        
            # cv.imshow('Craniovertebra Angle', frame)
            # if cv.waitKey(1) & 0xFF == 27:
            #     break #27 is ESC key
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # camera.release()
