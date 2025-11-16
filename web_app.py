"""
Physics Lab - Web Application
Flask-based web server with core physics modules
"""

from flask import Flask, render_template, request, jsonify
import math
import json
from datetime import datetime
from pathlib import Path
from modules.kinematics import Kinematics
from modules.freefall_dynamics import FreefallDynamics
from modules.work_energy import WorkEnergy
from modules.momentum import Momentum
from modules.electricity import Electricity
from modules.vectors import Vectors

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# History file
HISTORY_FILE = Path('data/history.json')

def load_history():
    """Load calculation history"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except (OSError, IOError):
        # Silently fail on read-only filesystem (Vercel)
        pass
    return []

def save_to_history(module, inputs, outputs):
    """Save calculation to history"""
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'module': module,
        'inputs': inputs,
        'outputs': outputs
    }
    try:
        history = load_history()
        history.append(entry)
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except (OSError, IOError, PermissionError):
        # Silently fail on read-only filesystem (Vercel)
        # Calculations still work, history just doesn't persist
        pass
    return entry

# ==================== KINEMATICS ====================
@app.route('/api/kinematics', methods=['POST'])
def kinematics():
    try:
        data = request.json
        u = float(data.get('u', 0))
        a = float(data.get('a', 0))
        t = float(data.get('t', 0))
        s = float(data.get('s', 0))
        v = float(data.get('v', 0))
        
        results = Kinematics.calculate(u=u, a=a, t=t, s=s, v=v)
        save_to_history('Kinematics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== FREEFALL DYNAMICS ====================
@app.route('/api/freefall', methods=['POST'])
def freefall():
    try:
        data = request.json
        h = float(data.get('h', 0))
        v0 = float(data.get('v0', 0))
        t = float(data.get('t', 0))
        g = float(data.get('g', 9.8))
        
        results = FreefallDynamics.calculate_freefall(h=h, v0=v0, t=t, g=g)
        save_to_history('Freefall Dynamics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== WORK AND ENERGY ====================
@app.route('/api/work_energy', methods=['POST'])
def work_energy():
    try:
        data = request.json
        force = float(data.get('force', 0))
        distance = float(data.get('distance', 0))
        mass = float(data.get('mass', 0))
        velocity = float(data.get('velocity', 0))
        height = float(data.get('height', 0))
        g = float(data.get('g', 9.8))
        
        results = WorkEnergy.calculate_work_energy(
            force=force, distance=distance, mass=mass, 
            velocity=velocity, height=height, g=g
        )
        save_to_history('Work and Energy', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== MOMENTUM ====================
@app.route('/api/momentum', methods=['POST'])
def momentum():
    try:
        data = request.json
        m1 = float(data.get('m1', 0))
        v1 = float(data.get('v1', 0))
        m2 = float(data.get('m2', 0))
        v2 = float(data.get('v2', 0))
        
        results = Momentum.calculate(m1=m1, v1=v1, m2=m2, v2=v2)
        save_to_history('Momentum', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== ELECTRICITY ====================
@app.route('/api/electricity', methods=['POST'])
def electricity():
    try:
        data = request.json
        calc_type = data.get('type', 'ohms')
        
        if calc_type == 'ohms':
            v = float(data.get('v', 0))
            i = float(data.get('i', 0))
            r = float(data.get('r', 0))
            results = Electricity.calculate_ohms_law(v=v, i=i, r=r)
        elif calc_type == 'coulombs':
            q1 = float(data.get('q1', 0))
            q2 = float(data.get('q2', 0))
            r = float(data.get('r', 1))
            results = Electricity.calculate_coulombs_law(q1=q1, q2=q2, r=r)
        else:
            results = {}
        
        save_to_history('Electricity', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== VECTORS ====================
@app.route('/api/vectors', methods=['POST'])
def vectors():
    try:
        data = request.json
        calc_type = data.get('type', 'magnitude')
        
        if calc_type == 'magnitude':
            x = float(data.get('x', 0))
            y = float(data.get('y', 0))
            z = float(data.get('z', 0))
            results = Vectors.calculate_vector_magnitude(x=x, y=y, z=z)
        elif calc_type == 'addition':
            x1 = float(data.get('x1', 0))
            y1 = float(data.get('y1', 0))
            x2 = float(data.get('x2', 0))
            y2 = float(data.get('y2', 0))
            results = Vectors.calculate_vector_addition(x1=x1, y1=y1, x2=x2, y2=y2)
        elif calc_type == 'dot':
            x1 = float(data.get('x1', 0))
            y1 = float(data.get('y1', 0))
            x2 = float(data.get('x2', 0))
            y2 = float(data.get('y2', 0))
            results = Vectors.calculate_dot_product(x1=x1, y1=y1, x2=x2, y2=y2)
        elif calc_type == 'angle':
            x1 = float(data.get('x1', 0))
            y1 = float(data.get('y1', 0))
            x2 = float(data.get('x2', 0))
            y2 = float(data.get('y2', 0))
            results = Vectors.calculate_angle_between(x1=x1, y1=y1, x2=x2, y2=y2)
        else:
            results = {}
        
        save_to_history('Vectors', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== HISTORY ====================
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        return jsonify(load_history())
    except Exception as e:
        return jsonify([])

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    try:
        HISTORY_FILE.write_text('[]')
        return jsonify({'status': 'cleared'})
    except (OSError, IOError):
        return jsonify({'status': 'cleared'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
