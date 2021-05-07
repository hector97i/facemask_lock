#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
# from camera import VideoCamera
import time
import threading
import os
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import pandas as pd
import time
from PIL import Image
# import serial
from datetime import datetime
# pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
# camera = cv2.VideoCapture('http://192.168.100.3:4747/video')


df = pd.DataFrame(columns=['mask','no_mask','time', 'image', 'prediction_confidence'])
cascPath = "models/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
model = load_model("models/mask_recog_ver2.h5")
# video_capture = cv2.VideoCapture('http://192.168.100.3:4747/video')

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return "HELLO WORLD!" #you can customze index.html here

# def gen(camera):
#     #get camera frame
#     while True:
#         ret, frame = camera.read()
#         frame = mask_detection(frame, True)
#         ret, img = cv2.imencode('.jpg', frame)
#         img = img.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

def genRequest(frame):
    #get camera frame
    prediction = mask_detection(frame, False)
    return prediction


# @app.route('/video_feed') 
# def video_feed():
#     return Response(gen(camera),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/prediction', methods = ['POST'])
def prediction():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {'error': 'No image submited'}
        try:
            f = request.files['file'].read()
            npimg = np.fromstring(f, np.uint8)
            frame = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            result = genRequest(frame)
            return result
        except Exception as e:
            return e


def add_mask():
    global df
    now=datetime.now()
    current_time = now.strftime("%H:%M:%S")
    img_path = '/with_mask/hasmask{}.jpg'.format(str(datetime.now()))
    pred = "{:.2f}%".format(max(mask, withoutMask) * 100)
    new_row={'mask':1, 'no_mask':0, 'time':current_time, 'image':img_path, 'prediction_confidence':pred}
    # cv2.imwrite(img_path,frame)

    # df=df.append(new_row, ignore_index=True)
    # df.to_csv('maskdata.csv', index = True)

def add_nomask():
    global df
    now=datetime.now()
    current_time = now.strftime("%H:%M:%S")
    img_path = '/without_mask/hasmask{}.jpg'.format(str(datetime.now()))
    pred = "{:.2f}%".format(max(mask, withoutMask) * 100)
    new_row={'mask':0, 'no_mask':1, 'time':current_time, 'image':img_path, 'prediction_confidence':pred}
    # cv2.imwrite(img_path,frame)

    # df=df.append(new_row, ignore_index=True)
    # df.to_csv('maskdata.csv', index = True)

    
def mask_detection(frame, image_flag):
    # Capture frame-by-frame
    # ret, frame = video_capture.read()
    label = ''
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
        faces_list=[]
        preds=[]
        for (x, y, w, h) in faces:
            face_frame = frame[y:y+h,x:x+w]
            face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
            face_frame = cv2.resize(face_frame, (224, 224))
            face_frame = img_to_array(face_frame)
            face_frame = np.expand_dims(face_frame, axis=0)
            face_frame =  preprocess_input(face_frame)
            faces_list.append(face_frame)
            if len(faces_list)>0:
                preds = model.predict(face_frame)
            else:
                return "NO FACES DETECTED"
            for pred in preds:
                (mask, withoutMask) = pred
            label = "Mask" if mask > withoutMask else "No Mask"
            # color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            if mask > withoutMask:
                print('MASK')
                # add_mask()

            else:
                print('NO MASK')
                # add_nomask()

            # cv2.putText(frame, label, (x, y- 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

            # cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)

        if image_flag:
            return frame
        else:
            return Response({res: label}, mimetype="application/json")

    except Exception as e:
        return e

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
    
