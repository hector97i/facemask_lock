import cv2
import os
import numpy as np
import pandas as pd
import time
from datetime import datetime

df = pd.DataFrame(columns=['mask', 'time', 'prediction_confidence'])
video_capture = cv2.VideoCapture('http://192.168.100.3:4747/video')

def add_mask():
    global df
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    pred = "{:.2f}%".format(max(mask, withoutMask) * 100)
    new_row = {'mask':1, 'time':current_time, 'prediction_confidence':pred}
    df = df.append(new_row, ignore_index=True)
    df.to_csv('maskdata.csv', index = True)

def add_nomask():
    global df
    now=datetime.now()
    current_time = now.strftime("%H:%M:%S")
    pred = "{:.2f}%".format(max(mask, withoutMask) * 100)
    new_row = {'mask':0, 'time':current_time, 'prediction_confidence':pred}
    df = df.append(new_row, ignore_index=True)
    df.to_csv('maskdata.csv', index = True)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    # SEND REQUEST AND WAIT FOR RESPONSE
    # resp = request(frame, ...)
    # EXTRACT PREDICTIONS FROM PAYLOAD
    # preds = resp.payload
    for pred in preds:
        (mask, withoutMask) = pred
    label = "Mask" if mask > withoutMask else "No Mask"
    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
    label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
    if mask > withoutMask:
        print('MASK')
        add_mask()

    else:
        print('NO MASK')
        add_nomask()
    
    # NOT SURE IF THIS WOULD WORK XD
    # cv2.putText(frame, label, (x, y- 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

    # cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)

    # cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
