from flask import render_template, Response, jsonify
from controllers.clark_angle import ClarkAngle
from controllers.craniovertebra_angle import CraniovertebraAngle
from controllers.forward_shoulder_angle import ForwardShoulderAngle
from controllers.carrying_angle import CarryingAngle
from controllers.q_angle import QAngle
from utils.save import Save

class Routes:
    def __init__(self, app):
        self.app = app
        self.cv = CraniovertebraAngle()
        self.fsa = ForwardShoulderAngle()
        self.carry = CarryingAngle()
        self.q = QAngle()
        self.clark = ClarkAngle()

    def setup(self):
        self.index()
        self.craniovertebra()
        self.forward_shoulder()
        self.carrying()
        self.q_angle()
        self.clark_angle()

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
            return Response(self.cv.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/save_cv')
        def save_cv():
            res = self.cv.results
            if res:
                Save.create('craniovertebra', res)
                return jsonify("success")
            else:
                return jsonify("failed")
            

    # Forward Shoulder Angle
    def forward_shoulder(self):
        @self.app.route('/forward_shoulder')
        def forward_shoulder():
            return render_template('forward_shoulder.html')

        @self.app.route('/forward_shoulder_vid')
        def forward_shoulder_vid():
            return Response(self.fsa.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/save_fsa')
        def save_fsa():
            res = self.fsa.results
            if res:
                Save.create('forward_shoulder', res)
                return jsonify("success")
            else:
                return jsonify("failed")
        
    def carrying(self):
        @self.app.route('/carrying')
        def carrying():
            return render_template('carrying.html')

        @self.app.route('/carrying_vid')
        def carrying_vid():
            return Response(self.carry.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/save_carry')
        def save_carry():
            res = self.carry.results
            if res:
                Save.create('carrying', res)
                return jsonify("success")
            else:
                return jsonify("failed")
            
    def q_angle(self):
        @self.app.route('/q_angle')
        def q_angle():
            return render_template('q_angle.html')
        
        @self.app.route('/q_angle_vid')
        def q_angle_vid():
            return Response(self.q.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/save_q')
        def save_q():
            res = self.q.results
            if res:
                Save.create('q_angle', res)
                return jsonify("success")
            else:
                return jsonify("failed")
            
    def clark_angle(self):
        @self.app.route('/clark_angle')
        def clark_angle():
            return render_template('clark_angle.html')
        
        @self.app.route('/clark_angle_vid')
        def clark_angle_vid():
            return Response(self.clark.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/save_clark')
        def save_clark():
            res = self.clark.results
            if res:
                Save.create('q_angle', res)
                return jsonify("success")
            else:
                return jsonify("failed")