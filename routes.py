from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps
import json
from datetime import datetime
import database
from config import REGIONS, REGIONS_FILE

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/zebra_crossing_analytics')
@login_required
def zebra_crossing_analytics():
    data = {}
    for cam_id in range(1, 5):
        data[f'cam{cam_id}'] = database.get_zebra_crossing_data(cam_id)
    return render_template('zebra_crossing.html', data=data)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'POST':
        data = request.json
        cam_id = data.get('cam_id')
        new_region = data.get('region')

        if not cam_id or not new_region:
            return jsonify({'status': 'error', 'message': 'Missing required data'}), 400

        REGIONS[cam_id]['Zebra'] = {
            'vertices': new_region['vertices'],
            'color': new_region.get('color', (0, 0, 255))
        }

        with open(REGIONS_FILE, 'w') as file:
            json.dump(REGIONS, file, indent=4)

        return jsonify({'status': 'success', 'message': f'Region updated for {cam_id}'}), 200

    return render_template('admin.html')

@app.route('/get_regions', methods=['GET'])
@login_required
def get_regions():
    return jsonify(REGIONS), 200