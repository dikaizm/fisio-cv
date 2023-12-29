import cv2 as cv
import mediapipe as mp
import math
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
        theta = math.atan2(y2 - y1, x2 - x1)
        degree = int(math.degrees(theta))

        return degree
    
    def find_midpoint(self, x1, y1, x2, y2):
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))
    
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
    
    def get_angle(self, fr, frame, keypoints, w, h, font, colors):
        l_shldr_x, l_shldr_y = keypoints["l_shldr_x"], keypoints["l_shldr_y"]
        r_shldr_x, r_shldr_y = keypoints["r_shldr_x"], keypoints["r_shldr_y"]
        nose_x = keypoints["nose_x"]
        
        green = colors["green"]
        red = colors["red"]
        yellow = colors["yellow"]
        pink = colors["pink"]
        
        # Calculate distance between left shoulder and right shoulder points.
        offset = self.find_distance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        
        # Assist to align the camera to point at the side view of the person.
        if offset < 50:
            cv.putText(frame, str(int(offset)) + ' Aligned', (10, h -50), font, 0.9, green, 2)
        else:
            cv.putText(frame, str(int(offset)) + ' Not Aligned', (10, h -50), font, 0.9, red, 2)
        
        # Get midpoint of left and right shoulder points.
        mx, _ = self.find_midpoint(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        
        cv.line(frame, (l_shldr_x, l_shldr_y), (r_shldr_x, r_shldr_y), yellow, 2)

        # Determine whether the person is facing left or right.
        if mx > nose_x:
            facing = 'left'
        else:
            facing = 'right'
            
        cv.putText(frame, 'Facing: ' + facing, (10, h - 20), font, 0.9, green, 2)


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
            
            self.show_landmarks(frame, lm)
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
