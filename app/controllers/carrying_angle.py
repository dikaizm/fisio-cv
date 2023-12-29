import cv2 as cv
import mediapipe as mp
import math
import numpy as np
from controllers.camera import Camera, Frame

class CarryingAngle:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_style = mp.solutions.drawing_styles

    def find_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def find_angle(self, x1, y1, x2, y2, facing = None):
        theta = math.acos( (y2 -y1)*(-y1) / (math.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
        degree = int(180/math.pi)*theta

        return degree
        
    def get_landmarks(self, frame):
        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.pose.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        lm = results.pose_landmarks
        lm_pose = self.mp_pose.PoseLandmark

        return lm, lm_pose
    
    def get_keypoints(self, lm, lm_pose, w, h):
        keypoints = {}
        # Left shoulder
        keypoints["l_shldr_x"] = int(lm.landmark[lm_pose.LEFT_SHOULDER].x * w)
        keypoints["l_shldr_y"] = int(lm.landmark[lm_pose.LEFT_SHOULDER].y * h)
        # Right shoulder
        keypoints["r_shldr_x"] = int(lm.landmark[lm_pose.RIGHT_SHOULDER].x * w)
        keypoints["r_shldr_y"] = int(lm.landmark[lm_pose.RIGHT_SHOULDER].y * h)
        # Left elbow
        keypoints["l_elbow_x"] = int(lm.landmark[lm_pose.LEFT_ELBOW].x * w)
        keypoints["l_elbow_y"] = int(lm.landmark[lm_pose.LEFT_ELBOW].y * h)
        # Right elbow
        keypoints["r_elbow_x"] = int(lm.landmark[lm_pose.RIGHT_ELBOW].x * w)
        keypoints["r_elbow_y"] = int(lm.landmark[lm_pose.RIGHT_ELBOW].y * h)
        # Left wrist
        keypoints["l_wrist_x"] = int(lm.landmark[lm_pose.LEFT_WRIST].x * w)
        keypoints["l_wrist_y"] = int(lm.landmark[lm_pose.LEFT_WRIST].y * h)
        # Right wrist
        keypoints["r_wrist_x"] = int(lm.landmark[lm_pose.RIGHT_WRIST].x * w)
        keypoints["r_wrist_y"] = int(lm.landmark[lm_pose.RIGHT_WRIST].y * h)
        # Nose
        keypoints["nose_x"] = int(lm.landmark[lm_pose.NOSE].x * w)
        
        return keypoints
    
    def show_landmarks(self, frame, lm):
        self.mp_draw.draw_landmarks(
            frame, 
            lm, 
            self.mp_pose.POSE_CONNECTIONS, 
            landmark_drawing_spec=self.mp_draw_style.get_default_pose_landmarks_style()
        )
    
    def draw_line_over(self, frame, center, radius, end_angle, direction, color = 'yellow'):
        # Convert angles to radians
        end_angle_rad = math.radians(end_angle)

        # Calculate end points of the line
        if direction == 1:
            end_point = (
                int(center[0] - radius * np.sin(end_angle_rad)),
                int(center[1] - radius * np.cos(end_angle_rad))
            )
        elif direction == -1:
            end_point = (
                int(center[0] + radius * np.sin(end_angle_rad)),
                int(center[1] + radius * np.cos(end_angle_rad))
            )
        
        cv.line(frame, center, end_point, color, 2)
    
    def get_angle(self, fr, frame, keypoints, w, h, font, colors):
        l_shldr_x, l_shldr_y = keypoints["l_shldr_x"], keypoints["l_shldr_y"]
        r_shldr_x, r_shldr_y = keypoints["r_shldr_x"], keypoints["r_shldr_y"]
        l_elbow_x, l_elbow_y = keypoints["l_elbow_x"], keypoints["l_elbow_y"]
        r_elbow_x, r_elbow_y = keypoints["r_elbow_x"], keypoints["r_elbow_y"]
        l_wrist_x, l_wrist_y = keypoints["l_wrist_x"], keypoints["l_wrist_y"]
        r_wrist_x, r_wrist_y = keypoints["r_wrist_x"], keypoints["r_wrist_y"]
        nose_x = keypoints["nose_x"]
        
        green = colors["green"]
        red = colors["red"]
        yellow = colors["yellow"]
        pink = colors["pink"]
        
        # Calculate distance between left shoulder and right shoulder points
        offset = self.find_distance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        
        # Assist to align the camera to point at the side view of the person
        if offset > 100:
            cv.putText(frame, str(int(offset)) + ' Aligned', (10, h -20), font, 0.9, green, 2)
        else:
            cv.putText(frame, str(int(offset)) + ' Not Aligned', (10, h -20), font, 0.9, red, 2)
        
        # Add circles
        cv.circle(frame, (l_shldr_x, l_shldr_y), 7, green, -1)
        cv.circle(frame, (r_shldr_x, r_shldr_y), 7, pink, -1)
        
        cv.circle(frame, (l_elbow_x, l_elbow_y), 7, green, -1)
        
        cv.circle(frame, (l_wrist_x, l_wrist_y), 7, green, -1)
        
        # Add line from left shoulder to right shoulder
        cv.line(frame, (l_shldr_x, l_shldr_y), (r_shldr_x, r_shldr_y), pink, 2)
        
        # Add vertical line from left shoulder
        cv.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y + 200), pink, 2)
        cv.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 50), pink, 2)
        
        # Get angle between left shoulder and left wrist
        elbow_shldr_angle = self.find_angle(l_elbow_x, l_elbow_y, l_shldr_x, l_shldr_y)    
        cv.putText(frame, str(int(elbow_shldr_angle)), (l_shldr_x - 50, l_shldr_y - 50), font, 0.9, green, 2)
        
        cv.line(frame, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), yellow, 2)
        
        # Distance between left shoulder and left wrist
        shldr_to_wrist = self.find_distance(l_shldr_x, l_shldr_y, l_wrist_x, l_wrist_y)
        
        # Draw line over upper arm
        self.draw_line_over(frame, (l_shldr_x, l_shldr_y), 200, elbow_shldr_angle, 1, yellow)
        self.draw_line_over(frame, (l_elbow_x, l_elbow_y), int(shldr_to_wrist), elbow_shldr_angle, -1, yellow)
        
        # Get angle between left elbow and left wrist
        wrist_elbow_angle = self.find_angle(l_wrist_x, l_wrist_y, l_elbow_x, l_elbow_y)
        cv.putText(frame, str(int(wrist_elbow_angle)), (l_elbow_x - 50, l_elbow_y - 50), font, 0.9, green, 2)
        
        cv.line(frame, (l_elbow_x, l_elbow_y), (l_wrist_x, l_wrist_y), yellow, 2)
        
        # Draw line over lower arm
        self.draw_line_over(frame, (l_elbow_x, l_elbow_y), 200, wrist_elbow_angle, 1, yellow)
        self.draw_line_over(frame, (l_wrist_x, l_wrist_y), 200, wrist_elbow_angle, -1, yellow)
        

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
            lm, lm_pose = self.get_landmarks(frame)
            if lm:
                keypoints = self.get_keypoints(lm, lm_pose, fr.width, fr.height)
                self.get_angle(fr, frame, keypoints, fr.width, fr.height, fr.font, fr.colors)
            
            # self.show_landmarks(frame, lm)
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
