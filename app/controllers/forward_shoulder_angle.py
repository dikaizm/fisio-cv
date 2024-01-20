from datetime import datetime
import time
import cv2 as cv
import math
from utils.theme import Colors
from utils.color_detection import ColorDetection, Point
from utils.camera import Camera, Frame

class ForwardShoulderAngle:
    def __init__(self):
        self.results = []

    def calc_angle(self, point1: Point, point2: Point):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        
        theta = math.acos( (y2 -y1)*(-y1) / (math.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
        degree = int(180/math.pi)*theta

        return degree
    
    def interpret(self, angle):
        if (angle <= 22):
            return 'normal'
        elif (angle >= 52):
            return 'forward shoulder'
        else:
            return ''
    
    def run(self):
        colors = Colors()
        detect = ColorDetection()
        fr = Frame()
        camera = Camera()
        camera.is_opened()
        
        while True:
            ret, frame = camera.get_frame()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            
            contours = detect.get_objects(frame)
            # Sort contours based on y-coordinate (top to bottom)
            contours = sorted(contours, key=lambda c: cv.boundingRect(c)[1])
            
            keypoints = []
            
            # Iterate over the contours and label them
            for i, contour in enumerate(contours, start=1):
                # Get the bounding box of the contour
                point_x, point_y, w, h = cv.boundingRect(contour)
                
                point = Point(point_x + w // 2, point_y + h // 2)

                keypoints.append(point)

                # Draw a rectangle around the detected object and label
                cv.rectangle(frame, (point_x, point_y), (point_x+w, point_y+h), colors.green, 2)
                fr.circle(frame, (point.x, point.y))
                fr.put_text(frame, str(i), (point.x + 10, point.y))
            #endfor
            
            # Connect keypoints with lines
            if len(keypoints) == 3:       
                # Draw vertical line from C7  
                fr.line(frame, (keypoints[1].x, keypoints[1].y), (keypoints[1].x, keypoints[1].y - 200))
                fr.line(frame, (keypoints[1].x, keypoints[1].y), (keypoints[1].x, keypoints[1].y + 200))
                
                # Draw line to each keypoints
                for i in range(len(keypoints) - 1):
                    fr.line(frame, (keypoints[i].x, keypoints[i].y), (keypoints[i + 1].x, keypoints[i + 1].y))
                    
                # Calculate the shoulder angle
                shoulder_angle = self.calc_angle(keypoints[2], keypoints[1])
                fr.put_text(frame, str(int(shoulder_angle)), (keypoints[1].x + 10, keypoints[1].y + 50), fontSize=1)
                
                fr.put_text(frame, 'Shoulder angle: ' + str(int(shoulder_angle)), (10, 50), fontSize=1.5)
                
                fr.put_text(frame, 'Condition: ' + self.interpret(shoulder_angle), (10, 100), fontSize=1.5)
                
                # Save results
                self.results.append((int(shoulder_angle), datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
            #endif
            
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # endwhile
