
import threading
import cv2
import os
from multiprocessing import Process, Pipe, Queue

# from camera_connect.machine_learning.webcam import stream_camera
from camera_connect.machine_learning.multiple_process.video_camera import CameraConfig, VideoCamera
from camera_connect.machine_learning.multiple_process.license_plate_detector import LicensePlateDetector
# from camera_connect.video_camera import start_streaming


def licensePlateRealtimeDetector():
    camera = VideoCamera(config = CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA"))
    license_detector = LicensePlateDetector()
    
    width = int(camera.video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(camera.video.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./output/', codec, fps, (width, height)) # output_path must be .mp4
    no_of_frames = int(camera.video.get(cv2.CAP_PROP_FRAME_COUNT))

    original_frames = Queue()
    Frames_data = Queue()
    Predicted_data = Queue()
    Processed_frames = Queue()
    Processing_times = Queue()
    Final_frames = Queue()


    input_process = Process(target=camera.update, args=(Frames_data, Predicted_data, Processing_times))
    process_process = Process(target=license_detector.detect, args=(Predicted_data, original_frames, Processed_frames, Processing_times, input_size, CLASSES, score_threshold, iou_threshold, rectangle_colors, realtime))
    output_process = Process(target=Show_Image_mp, args=(Processed_frames, show, Final_frames))
    input_process.start()
    process_process.start()
    output_process.start()
        
