from flask import Flask, render_template, Response
from PushUpCounter import PushUpCounter
from BicepCurlCounter import BicepCurlCounter
from CurlUpCounter import CurlUpCounter
from SquatsCounter import SquatsCounter
from PlankCounter import PlankCounter

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

def gen(camera):
  while True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame
           + b'\r\n\r\n')

@app.route('/push_ups')
def push_up():
  return Response(gen(PushUpCounter()), 
                  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/curl_ups')
def curl_ups():
  return Response(gen(CurlUpCounter()), 
                  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/bicep_curls')
def bicep_curls():
  return Response(gen(BicepCurlCounter()), 
                  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squats')
def squats():
  return Response(gen(SquatsCounter()),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/planks')
def planks():
  return Response(gen(PlankCounter()),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='5000', debug=True)