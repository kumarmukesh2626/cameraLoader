from getlatestframes import CameraLoader
import cv2
import base64
from PIL import Image
import io
import json
import requests


test_batch_url =  'http://localhost:5000/api/v1/objectdetection'
video_capture = CameraLoader('config/cam_config.ini')
video_capture.start()

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



while True:
    myobj = []
    for camera_id, frames in video_capture.frame_set.items():
        if frames:
            latest_frame = frames[-1]
            image = imageToBase64String(latest_frame)
            myobj.append({"CamID": 'cam1',
                        "frame": str(image)
                        })
            response = requests.post(test_batch_url, json=myobj)
            print("response", response)
            json_data = json.loads(response.text)
            

