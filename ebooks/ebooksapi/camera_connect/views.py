# Create your views here.
import time
import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.gzip import gzip_page

from multiprocessing import Process, Pipe, Queue
import imutils
from imutils.video import WebcamVideoStream, FPS
from camera_connect.machine_learning.multiprocessing_camera_video_stream import MultiprocessingCameraVideoStream
import traceback
import datetime

# from camera_connect.machine_learning.webcam import stream_camera
from camera_connect.machine_learning.multiple_process.video_camera import CameraConfig, VideoCamera
from camera_connect.machine_learning.multiple_process.license_plate_detector import LicensePlateDetector
# from camera_connect.video_camera import start_streaming

# from camera_connect.machine_learning.license_plate_detector import LicensePlateDetector
# Create your views here.
def stream():
    ip_address="10.86.7.123"
    username="admin"
    password="123456aA"
    # cap = cv2.VideoCapture(0) 
    cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip_address}/1')
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')



def camera(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def Read_Camera(original_frames: Queue):
    """_summary_
    """
    camera = VideoCamera(config = CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA"))
    
    # width = int(camera.video.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(camera.video.get(cv2.CAP_PROP_FPS))
    # codec = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('./output/', codec, fps, (width, height)) # output_path must be .mp4
    # no_of_frames = int(camera.video.get(cv2.CAP_PROP_FRAME_COUNT))
    camera.run(queue=original_frames)
    
    
def Detect_Plate(original_frames: Queue, processed_frames: Queue):
    """_summary_
    """   
    license_detector = LicensePlateDetector()
    
    while True:
        processing_frame = original_frames.get()
        if processing_frame is not None:
            processed_frame = license_detector.detect(frame=processing_frame)
            output = processed_frame
            if processed_frame is None:
                output = processing_frame
            processed_frames.put(output)
    
     
    
def Show_Result(processed_frames,):
    """_summary_
    """
    
    while True:
        if processed_frames.qsize() > 0:
            frame = processed_frames.get()
            _, jpeg = cv2.imencode('.jpg', frame)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    
    
    
def start_streaming():
    
    original_frames = Queue()
    # Frames_data = Queue()
    # Predicted_data = Queue()
    Processed_frames = Queue()
    # Processing_times = Queue()
    # Final_frames = Queue()

    input_process = Process(target=Read_Camera, args=(original_frames,))
    input_process.start()
    process_process = Process(target=Detect_Plate, args=(original_frames, Processed_frames,))
    process_process.start()
    # output_process = Process(target=Show_Result, args=(Processed_frames,))
    # output_process.start()
    
    # # original_frames.put(camera.get_raw_frame())
    # camera = VideoCamera(config = CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA"))
    # width = int(camera.video.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(camera.video.get(cv2.CAP_PROP_FPS))
    # codec = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('./output/', codec, fps, (width, height)) # output_path must be .mp4
    # no_of_frames = int(camera.video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # camera.run(queue=original_frames)
        
    while True:
        # if original_frames.qsize() == 0 and Processed_frames.qsize() == 0:
        #     # input_process.terminate()
        #     process_process.terminate()
        #     output_process.terminate()
        #     break
        #     """
        #     """
        #     # time.sleep(0.1)
        # elif Processed_frames.qsize() > 0:
        # if Processed_frames.qsize() > 0:
        try: 
            frame = Processed_frames.get()
            if frame is not None:
                _, jpeg = cv2.imencode('.jpg', frame)
                yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        except:
            pass
        
def start_streaming_imutils_thread():
    license_detector = LicensePlateDetector()
    # camera = MultiprocessingCameraVideoStream(src=CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA").__str__())
    camera = WebcamVideoStream(src=CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA").__str__())
    camera.start()
    # fps = FPS()
    _previous_time_frame = 0
    _new_time_frame = 0
    while True:
        try: 
            # fps.start()
            
            processing_frame = camera.read()
            # fps.update()
            processing_frame = imutils.resize(processing_frame, width=640)
            processed_frame = license_detector.detect(frame=processing_frame)
            output = None
            if processed_frame is None:
                output = processing_frame
            else:    
                output = processed_frame
            # fps.stop()
            _new_time_frame = time.time()
            
            _fps_ = 1 / (_new_time_frame - _previous_time_frame)
            cv2.putText(output, str("FPS {:.2f}".format(_fps_)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            _, jpeg = cv2.imencode('.jpg', output)
            _previous_time_frame = _new_time_frame
            
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        except Exception:
            print(traceback.format_exc()) 
            pass
        
    cv2.destroyAllWindows()
    camera.stop()
    
def start_streaming_1_thread():
    cv2.ocl.setUseOpenCL(True)
    
    camera = VideoCamera(config = CameraConfig(ip_address="10.86.7.123",username="admin",password="123456aA"))
    license_detector = LicensePlateDetector()

    while camera.video.isOpened():
        try:
            processing_frame = camera.get_raw_frame()
            processed_frame = license_detector.detect(frame=processing_frame)
            output = None
            if processed_frame is None:
                output = processing_frame
            else:    
                output = processed_frame
            _, jpeg = cv2.imencode('.jpg', output)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        except:
            pass
        
@gzip_page
def video_feed(request):
    # return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
    
    # return StreamingHttpResponse(streaming_content=start_streaming(), content_type='multipart/x-mixed-replace; boundary=frame')
    # return StreamingHttpResponse(streaming_content=start_streaming_1_thread(), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(streaming_content=start_streaming_imutils_thread(), content_type='multipart/x-mixed-replace; boundary=frame')
