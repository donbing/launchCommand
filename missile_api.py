from importlib import import_module
import os
from flask import Flask, render_template, request, redirect, url_for, Response
from missile import MissileLauncher

#try:
  #Camera = import_module('camera_pi').Camera
#except:
Camera = import_module('camera_opencv').Camera

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


