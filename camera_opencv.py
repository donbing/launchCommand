import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        overlay = cv2.imread('static/crosshair2.png')
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            added_image = cv2.addWeighted(img[190:290,270:370,:], 1, overlay[0:100,0:100,:], 0.1, 0)
            img[190:290,270:370] = added_image
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()