
import cv2
import os
from multiprocessing import Queue, Process


class CameraConfig(object):
    # ip_address="10.86.7.123"
    # username="admin"
    # password="123456aA"
    
    def __init__(self, ip_address:str, username:str, password:str):
        self.ip_address=ip_address
        self.username=username
        self.password=password
        
        
    def __str__(self) -> str:
        return f'rtsp://{self.username}:{self.password}@{self.ip_address}/1'

class VideoCamera(object):
    def __init__(self, config: CameraConfig):
        
        self.config = config
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(f'rtsp://{self.config.username}:{self.config.password}@{self.config.ip_address}/1')
        
        self.video.set(3, 640)
        self.video.set(4, 480)
        self.grabbed = None
        self.frame = None
        # self.p1 = Process(target=self.update)
        # self.p1.start()

    def __del__(self):
        self.video.release()
        # self.p1.terminate()
    
    def video_cam(self) -> cv2.VideoCapture:
        return self.video
        
    def get_raw_frame(self):
        (self.grabbed, self.frame) = self.video.read()
        return self.frame
        
    def get_frame(self):
        image = self.get_raw_frame()
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def run(self, queue: Queue = None):
        
        # (self.grabbed, self.frame) = self.video.read()
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if queue is not None:
                queue.put(self.frame)
            