import requests
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

base_url = '35.236.20.13'


class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def post_image(self):
        img = self.get_frame()
        url = 'http://' + base_url + '/predict'
        files = {'file': img}
        response = requests.post(url, files=files)
        print(response)

def main():
    
    pi_camera = VideoCamera(flip=False) 
    # base_url = input('Server URL: ') + ':5000'

    while True:
        print('Requesting prediction to http://' + base_url + '/predict')
        res = pi_camera.post_image()
        print(f"RESULT: {res}")
        time.sleep(5)


if __name__ == '__main__':
    main()
