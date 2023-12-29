from flask import render_template, Response
from controllers.craniovertebra_angle import CraniovertebraAngle
from controllers.forward_shoulder_angle import ForwardShoulderAngle
from controllers.carrying_angle import CarryingAngle
from controllers.camera import Camera

class Routes:
    def __init__(self, app):
        self.app = app

    def setup(self):
        self.index()
        self.craniovertebra()
        self.forward_shoulder()
        self.carrying()

    # Home
    def index(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

    # Craniovertebra Angle
    def craniovertebra(self):
        @self.app.route('/craniovertebra')
        def craniovertebra():
            return render_template('craniovertebra.html')

        @self.app.route('/craniovertebra_vid')
        def craniovertebra_vid():
            return Response(CraniovertebraAngle().run(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # Forward Shoulder Angle
    def forward_shoulder(self):
        @self.app.route('/forward_shoulder')
        def forward_shoulder():
            return render_template('forward_shoulder.html')

        @self.app.route('/forward_shoulder_vid')
        def forward_shoulder_vid():
            return Response(ForwardShoulderAngle().run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
    def carrying(self):
        @self.app.route('/carrying')
        def carrying():
            return render_template('carrying.html')

        @self.app.route('/carrying_vid')
        def carrying_vid():
            return Response(CarryingAngle().run(), mimetype='multipart/x-mixed-replace; boundary=frame')