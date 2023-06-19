# Create your views here.
import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from camera_connect.camera.webcam import stream_camera
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

def video_feed(request):
    # return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(stream_camera(ip_address="10.86.7.123",username="admin",password="123456aA"), content_type='multipart/x-mixed-replace; boundary=frame')


def camera(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
