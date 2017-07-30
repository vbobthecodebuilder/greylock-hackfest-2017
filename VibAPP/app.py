from flask import Flask, render_template, Response, redirect, jsonify
import cv2
import sys

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

@app.route('/')
def test():
    return render_template('test.html')


@app.route('/mix')
def index():
    return redirect("http://127.0.0.1:8888", code=302)

currentCommand = 1


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'currentCommand': currentCommand})

def gen_from_cam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            area = w*h
            if area > 100000:
                print("big")
            else:
                print("small")
        cv2.imwrite("test.jpg", frame)
        f = open("test.jpg", 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_from_cam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

