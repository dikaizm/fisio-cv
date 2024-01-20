import cv2 as cv
from utils.theme import Colors

class Camera:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
    
    def is_opened(self):
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self):
        print('Finished.')
        self.cap.release()
        cv.destroyAllWindows()
        
global_colors = Colors()

class Frame:    
    def __init__(self):
        self.font = cv.FONT_HERSHEY_SIMPLEX
    
    def put_text(self, frame, label, position, fontSize = 0.8):
        cv.putText(frame, label, position, self.font, fontSize, global_colors.yellow, 2)
        
    def line(self, frame, start_point, end_point, color = global_colors.yellow):
        cv.line(frame, start_point, end_point, color, 4)
        
    def circle(self, frame, center, color = global_colors.pink):
        cv.circle(frame, center, 7, color, -1)