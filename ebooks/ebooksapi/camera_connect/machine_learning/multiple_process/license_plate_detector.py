import cv2
import torch
import math 
import os
import time
import argparse
from IPython.display import display
from PIL import Image
from camera_connect.machine_learning.function import utils_rotate as utils_rotate
from camera_connect.machine_learning.function import helper as helper

class LicensePlateDetector(object):
    def __init__(self):
        crrDir = os.getcwd()
        camera_path = f'{crrDir}/ebooksapi/camera_connect/machine_learning'
        # load model
        self.yolo_LP_detect = torch.hub.load(f'{camera_path}/yolov5', 'custom', path=f'{camera_path}/model/LP_detector_nano_61.pt', force_reload=True, source='local')
        print('===================== 1 =========================')
        self.yolo_license_plate = torch.hub.load(f'{camera_path}/yolov5', 'custom', path=f'{camera_path}/model/LP_ocr_nano_62.pt', force_reload=True, source='local')
        print('===================== 2 =========================')
        self.yolo_license_plate.conf = 0.60

    def detect(self, frame):
        try:
            plates = self.yolo_LP_detect(frame, size=640)
            list_plates = plates.pandas().xyxy[0].values.tolist()
            list_read_plates = set()
            for plate in list_plates:
                flag = 0
                x = int(plate[0]) # xmin
                y = int(plate[1]) # ymin
                w = int(plate[2] - plate[0]) # xmax - xmin
                h = int(plate[3] - plate[1]) # ymax - ymin  
                crop_img = frame[y:y+h, x:x+w]
                cv2.rectangle(frame, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
                lp = ""
                for cc in range(0,2):
                    for ct in range(0,2):
                        lp = helper.read_plate(self.yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                        if lp != "unknown":
                            list_read_plates.add(lp)
                            cv2.putText(frame, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                            flag = 1
                            break
                    if flag == 1:
                        break
            new_frame_time = time.time()
            fps = 1/(new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            return frame
        except:
            pass
        