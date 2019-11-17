from flask import Flask, render_template, request, redirect, url_for, Response
from missile import MissileLauncher
import picamera, time, io, threading


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (640, 480)
            

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None


launcher = MissileLauncher()

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/move/<action>', methods=['POST'])
def move(action):
    method = getattr(launcher, action, lambda: "nothing")
    duration = request.form.get('duration', type=int)
    method(duration)
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    launcher.stop()    
    return redirect(url_for('index'))

@app.route('/fire', methods=['POST'])
def fire():
    launcher.fire()    
    return redirect(url_for('index'))

@app.route('/video_feed.mjpeg')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #video/x-motion-jpeg

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


