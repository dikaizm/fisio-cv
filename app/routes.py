from flask import render_template, Response, jsonify
from controllers.craniovertebra_angle import CraniovertebraAngle
from controllers.forward_shoulder_angle import ForwardShoulderAngle
from controllers.carrying_angle import CarryingAngle
from controllers.camera import Record

class Routes:
    def __init__(self, app):
        self.app = app
        self.cv = CraniovertebraAngle()
        self.fsa = ForwardShoulderAngle()
        self.carry = CarryingAngle()

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
            return Response(self.cv.run(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/record_cv')
        def record_cv():
            res = self.cv.results
            if res:
                Record.save_result('craniovertebra', res)
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
        
        @self.app.route('/record_fsa')
        def record_fsa():
            res = self.fsa.results
            if res:
                Record.save_result('forward_shoulder', res)
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
        
        @self.app.route('/record_carry')
        def record_carry():
            res = self.carry.results
            if res:
                Record.save_result('carrying', res)
                return jsonify("success")
            else:
                return jsonify("failed")