from flask import Flask, render_template, request, Response, redirect, url_for
from controllers.craniovertebra_angle import CraniovertebraAngle
from controllers.camera import Camera

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Craniovertebra Angle
@app.route('/craniovertebra')
def craniovertebra():
    return render_template('craniovertebra.html')

@app.route('/craniovertebra_vid')
def craniovertebra_vid():
    return Response(CraniovertebraAngle().run(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Forward Shoulder Angle
@app.route('/forward_shoulder')
def forward_shoulder():
    return render_template('forward_shoulder.html')

@app.route('/forward_shoulder_vid')
def forward_shoulder_vid():
    return Response(Camera().generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=True)