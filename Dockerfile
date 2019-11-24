FROM balenalib/raspberry-pi-python
WORKDIR /usr/src/app
RUN sudo apt-get update
RUN sudo apt-get install python-opencv
RUN pip install flask
RUN pip install pyusb
RUN pip install picamera
COPY . .
EXPOSE 5000
CMD [ "python", "./missile_api.py" ]