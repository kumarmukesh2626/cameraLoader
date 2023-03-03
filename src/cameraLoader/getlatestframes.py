import time
import cv2
import numpy as np
from imutils.video import FPS
import pandas as pd
from queue import Queue
from threading import Thread
import cv2
from collections import deque
from cameraLoader.fetch_config_values import MyParser
import config.config_log as cf
from ensure import ensure_annotations


class CameraLoader:
    """
    Class for getting video frames from a video source using a dedicated thread.

    Attributes:
        config (MyParser): Object for parsing a configuration file.
        config_setting (dict): Dictionary of configuration settings.
        video_objects (dict): Dictionary of video capture objects and their properties.
        frame_set (dict): Dictionary of video frames from each capture object.
        stopped (bool): Flag for stopping the frame capture thread.

    Methods:
        start(): Start the frame capture thread.
        get(): Continuously get video frames.
        stop(): Stop the frame capture thread.
    """

    def __init__(self, config_file_path):
        self.config = MyParser()
        self.config.read(config_file_path)
        self.log_path = self.config["LOG Related"]["LOG_FILE_PATH"]
        self.config_setting = self.config.as_dict()
        self.video_objects = {}
        for cam in self.config_setting.keys():
            if 'rtsp' not in self.config_setting[cam]:
                cf.error_log(400, "Rtsp link not found for camera", "CameraLoader", self.log_path)
                print(f"rtsp link not found for camera {cam}")
                continue
            try:
                cf.success_log(200, "Reading the Video Capture", "CameraLoader", self.log_path)
                cap = cv2.VideoCapture(self.config_setting[cam]['rtsp'])
                if cap.isOpened():
                    try:
                        cap_obj = {"config_key": cam,
                                   "cameraID": self.config_setting[cam]['cameraid'],
                                   "nfps": int(cap.get(cv2.CAP_PROP_FPS)),
                                   "size": (int(cap.get(3)), int(cap.get(4))),
                                   "capture_obj": cap}
                    except KeyError as e:
                        cf.error_log(400, "Missing camrea Property", "CameraLoader", self.log_path)
                        print(f"Missing property {e} for camera {cam}")
                    self.video_objects[cap_obj["cameraID"]] = cap_obj
            except Exception as e:
                cf.error_log(400, "Error in Opening Camera", "CameraLoader", self.log_path)
                print(f"Error opening camera: {e}")

        self.frame_set = {}
        for idx, cap_obj in enumerate(self.video_objects.values()):
            self.frame_set[cap_obj["cameraID"]] = deque(maxlen=1)
        self.stopped = False

    @ensure_annotations
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    @ensure_annotations
    def get(self):
        while not self.stopped:
            for cap_obj in self.video_objects.values():
                try:
                    cf.success_log(200, "Reading the capture object", "CameraLoader", self.log_path)
                    ret, frame = cap_obj["capture_obj"].read()
                    if ret:
                        self.frame_set[cap_obj["cameraID"]].append(frame)
                except Exception as e:
                    print(f"Error getting frame: {e}")

    @ensure_annotations
    def stop(self):
        self.stopped = True


'''
how to run code

video_capture = CameraLoader(cameras)
video_capture.start()


while True:
    for key, value in video_capture.frame_set.items():
        if value:
            frame = value[0]
            # do something with the frame
    if end_condition:
        video_capture.stop()
        break


'''
'''
while True:
    # continuously retrieve the latest frame for each camera
    for camera_id, frame_deque in camera_loader.frame_set.items():
        print(camera_id)
        if frame_deque:
            latest_frame = frame_deque[-1]
            dt = datetime.now()
            imgname = camera_id +str(dt.date())+"_"+str(dt.hour)+\
                                            '-'+str(dt.minute)+'-'+str(dt.second)+'_'+\
                                            str(dt.microsecond//1000)
            imgname += '_iocl.jpg'
            cv2.imwrite(os.path.join(folder_less_confidence, imgname),latest_frame)
            print("image saved")
    time.sleep(sleep)

'''
