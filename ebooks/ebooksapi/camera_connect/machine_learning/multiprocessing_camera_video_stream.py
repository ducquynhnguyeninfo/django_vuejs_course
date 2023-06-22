# from threading import Thread
from multiprocessing import Queue, Process
import cv2

class MultiprocessingCameraVideoStream:
    def __init__(self, src=0, name = 'MultiprocessingCameraVideoStream'):
        self.src=src
        # initialize the video camera stream
        self.name = name
        self.stream = None
        self.grabbed = None
        self.frame = None
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        
        self.start()
        
        
    def start(self):
        # start the thread to read frames from the video stream
        p = Process(target=self.update, name=self.name, args=())
        p.daemon=True
        p.start()
        return self
    
    def update(self):
        # initialize the video camera stream 
        self.stream = cv2.VideoCapture(self.src)
        # read the first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()
        
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            
    def read(self):
        # return the frame most recently read
        return self.frame
    
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True