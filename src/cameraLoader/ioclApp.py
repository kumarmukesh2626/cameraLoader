#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:02:36 2022

@author: Mukesh
"""

'''
API based approach to run models on images.
    Developer: Mukesh
    Company: Algo8AI
    Date: 20-Nov-2022
'''
from PIL import Image
import numpy as np
import io
import torch
from waitress import serve
from flask_cors import CORS
from flask import Flask, jsonify, request
import time
import random
import configparser
from logs.configuration_file import success_log, error_log



def stringToRGB(base64_string):
    try:
        imgdata = base64.b64decode(str(base64_string))
        img = Image.open(io.BytesIO(imgdata))
        opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        return (True, opencv_img)
    except:
        return (False, "not able to retrieve image")


def imageToBase64String(img):
    _, buffer = cv2.imencode('.jpg', img)
    return str(base64.b64encode(buffer).decode('utf-8'))


#  creating flask app to host the api's at
app = Flask(__name__)
# cors initialization so that all modern browsers can identify as url (*not required for API development*)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# post api which accepts inputs as follows

@app.route('/api/v1/objectdetection', methods=['POST'])
def batch_automation():
    success_log("POST method call successful", "201", "main.automation")
    start = time.time()
    # read json data send via api
    success_log("reading json data from api", "202", "__main__")
    batch_data = request.json
    batch_camids = []
    batch_images = []
    camera_id = []
    #  fetching both camid and frame
    for img_data in batch_data:
        frame = img_data["frame"]
        camid = img_data["CamID"]
        print("Received : {}".format(camid))
        # converting base64 frame to cv2 image so that it can be used via YOLOv5 model
        t = time.time()
        success_log("Frame Received of camera :{} {}".format(camid, t - start), "205", "automation")
        b64_time = time.time()
        status, original_frame = stringToRGB(frame)
        b64_end_time = time.time()
        success_log("time taken to convert frame" + str(b64_end_time - b64_time), "205", "automation")
        success_log("total time taken for current instances" + str(b64_end_time - start), "205", "automation")
        if status == False:
            error_log("Base64 to image converstion failed.", "500", "automation.stringToRGB")
            return jsonify({
                "Status": False,
                "Message": "Check image not able to decrypt base64 image. Try removing 'data:image/png;base64,' from frames"
            }), 500
        else:
            batch_images.append(original_frame)
            frames = imageToBase64String(original_frame)
            camera_id.append(camid)
            batch_res = ({"frame": frames,
                          "cameraID": camid
                          })
            batch_camids.append(batch_res)
    # running model
    t1 = time.time()
    success_log("parsing frames to YOLOv5", "203", "__main__.automation")
    success_log("Parsing Frame into model:{} {}".format(camera_id, t1 - start), "205", "automation")
    print("Parsing Frame into model:{} {}".format(camera_id, t1 - start))
    results = net(batch_images)
    t1_model = time.time()  
    success_log("completion of process in yolov5 model" + str(t1_model - t1), "205", "automation")
    print("completion of process in yolov5 model" + str(t1_model - t1))
    #  fetching data in correct json format
    batch_out_json = []
    for i, batch_res in enumerate(batch_camids):
        outs = results.pandas().xyxy[i].to_dict(orient="records")
        print("outs",outs)
        batch_out_json.append({
            "Status": True,
            "Message": "All process success",
            "Results": outs,
            "cameraID": batch_res["cameraID"],
            "frame": batch_res["frame"],
        })
    success_log("Model response recorded.", "204", "__main__.automation")
    end = time.time()
    success_log("Time taken to generate and send response :{}".format(end - start), "205", "automation")
    #  if everthing works fine send positive response to the client
    return jsonify(batch_out_json), 200
    #  exception handling if something fails in code

if __name__ == '__main__':
    success_log("initialising flask api.", "101", "__main__")
    # calling config parameters in the code 
    try:
        try:
            config_value = configparser.ConfigParser()
            config_value.read('config/common_config.ini')
            model_dir = config_value["model"]["model_dir"]
            weights = config_value["model"]["weights"]
            conf = float(config_value['configuration']['confidence'])
            success_log("Config values for model picked up.", "102", "__main__")
        except:
            error_log("Not able to fetch config file/values.", "500", "__main__")
        success_log("Initalizing YOLOv5 model", "103", "__main__")
        net = torch.hub.load(model_dir, 'custom', path=weights, source='local', _verbose=False,force_reload=True)
        net.conf = conf
        #  run server based on values in config file
        if config_value["API"]["API_instance"] == "PROD":
            success_log("running API in production mode.", "200", "__main__")
            serve(app, port=5000)
        elif config_value["API"]["API_instance"] == "DEBUG":
            success_log("running API in development mode", "200", "__main__")
            app.run(host="0.0.0.0", port=5000, debug=True)
        else:
            success_log("running API in testing mode. debug is off.", "200", "__main__")
            app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(e)
        error_log("Flask api initalization failed.", "500", "__main__")