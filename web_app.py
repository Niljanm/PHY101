"""
Physics Lab - Web Application
Flask-based web server for the Physics Calculator
"""

from flask import Flask, render_template, request, jsonify
import math
import json
from datetime import datetime
from pathlib import Path
from utils.unit_converter import UnitConverter

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# History file
HISTORY_FILE = Path('data/history.json')

def load_history():
    """Load calculation history"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_to_history(module, inputs, outputs):
    """Save calculation to history"""
    history = load_history()
    entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'module': module,
        'inputs': inputs,
        'outputs': outputs
    }
    history.append(entry)
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
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
        
        results = {}
        
        if t != 0:
            results['v'] = u + a * t
        if s != 0 and a != 0:
            v_squared = u**2 + 2*a*s
            if v_squared >= 0:
                results['v'] = math.sqrt(v_squared)
        if a != 0 and (v != 0 or u != 0):
            results['t'] = (v - u) / a
        if t != 0 and a != 0:
            results['s'] = u*t + 0.5*a*t**2
        if t != 0 and (u != 0 or v != 0):
            results['s'] = (u + v) * t / 2
        
        save_to_history('Kinematics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== OHM'S LAW ====================
@app.route('/api/ohms_law', methods=['POST'])
@app.route('/api/ohms-law', methods=['POST'])
def ohms_law():
    try:
        data = request.json
        V = float(data.get('V', 0))
        I = float(data.get('I', 0))
        R = float(data.get('R', 0))
        
        results = {}
        
        if I and R:
            results['V'] = I * R
        if V and R and R != 0:
            results['I'] = V / R
        if V and I and I != 0:
            results['R'] = V / I
        
        # Power calculations
        if V and I:
            results['P'] = V * I
        if I and R:
            results['P'] = I**2 * R
        if V and R and R != 0:
            results['P'] = V**2 / R
        
        save_to_history("Ohm's Law", data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== ENERGY ====================
@app.route('/api/energy', methods=['POST'])
def energy():
    try:
        data = request.json
        m = float(data.get('m', 0))
        v = float(data.get('v', 0))
        g = float(data.get('g', 9.8))
        h = float(data.get('h', 0))
        
        results = {}
        
        if m > 0 and v >= 0:
            results['KE'] = 0.5 * m * v**2
        if m > 0 and h >= 0:
            results['PE'] = m * g * h
        if m > 0 and v >= 0 and h >= 0:
            results['ME'] = 0.5*m*v**2 + m*g*h
        
        save_to_history('Energy', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== MOMENTUM ====================
@app.route('/api/momentum', methods=['POST'])
def momentum():
    try:
        data = request.json
        m1 = float(data.get('m1', 0))
        v1 = float(data.get('v1', 0))
        m2 = float(data.get('m2', 0))
        v2 = float(data.get('v2', 0))
        
        results = {}
        
        if m1 > 0:
            results['p1'] = m1 * v1
        if m2 > 0:
            results['p2'] = m2 * v2
        if m1 > 0 and m2 > 0:
            results['p_total'] = m1*v1 + m2*v2
        
        save_to_history('Momentum', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== OPTICS ====================
@app.route('/api/optics', methods=['POST'])
def optics():
    try:
        data = request.json
        f = float(data.get('f', 0))
        u = float(data.get('u', 0))
        v = float(data.get('v', 0))
        
        results = {}
        
        if u > 0 and f > 0 and u != f:
            results['v'] = (u * f) / (u - f)
        if f > 0 and v > 0 and v != f:
            results['u'] = (v * f) / (v - f)
        if u > 0 and v != 0:
            results['m'] = -v / u
        if u > 0 and v > 0 and (u + v) != 0:
            results['f'] = (u * v) / (u + v)
        
        save_to_history('Optics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== THERMODYNAMICS ====================
@app.route('/api/thermodynamics', methods=['POST'])
def thermodynamics():
    try:
        data = request.json
        m = float(data.get('m', 0))
        c = float(data.get('c', 0))
        delta_t = float(data.get('delta_t', 0))
        
        results = {}
        
        if m and c and delta_t:
            results['Q'] = m * c * delta_t
        
        save_to_history('Thermodynamics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== CIRCULAR MOTION ====================
@app.route('/api/circular_motion', methods=['POST'])
@app.route('/api/circular-motion', methods=['POST'])
def circular_motion():
    try:
        data = request.json
        m = float(data.get('m', 0))
        v = float(data.get('v', 0))
        r = float(data.get('r', 0))
        omega = float(data.get('omega', 0))
        
        results = {}
        
        if m and v and r and r != 0:
            results['F_c'] = (m * v**2) / r
            results['a_c'] = (v**2) / r
        if v and r and r != 0:
            results['omega'] = v / r
        if omega and r:
            results['v'] = omega * r
        
        save_to_history('Circular Motion', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== PROJECTILE MOTION ====================
@app.route('/api/projectile_motion', methods=['POST'])
@app.route('/api/projectile-motion', methods=['POST'])
def projectile_motion():
    try:
        data = request.json
        v0 = float(data.get('v0', 0))
        theta = float(data.get('theta', 0))
        g = float(data.get('g', 9.8))
        
        results = {}
        
        if v0 and theta:
            theta_rad = math.radians(theta)
            results['max_height'] = (v0**2 * math.sin(theta_rad)**2) / (2 * g)
            results['range'] = (v0**2 * math.sin(2*theta_rad)) / g
            results['time_of_flight'] = (2 * v0 * math.sin(theta_rad)) / g
        
        save_to_history('Projectile Motion', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== SIMPLE HARMONIC MOTION ====================
@app.route('/api/shm', methods=['POST'])
def shm():
    try:
        data = request.json
        m = float(data.get('m', 0))
        k = float(data.get('k', 0))
        A = float(data.get('A', 0))
        
        results = {}
        
        if m and k and m > 0:
            omega = math.sqrt(k / m)
            results['omega'] = omega
            results['T'] = 2 * math.pi / omega
            results['f'] = 1 / results['T']
        if k and A:
            results['E'] = 0.5 * k * A**2
        if m and k:
            results['max_v'] = math.sqrt(k / m) * A if A else 0
        
        save_to_history('SHM', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== ELECTROSTATICS ====================
@app.route('/api/electrostatics', methods=['POST'])
def electrostatics():
    try:
        data = request.json
        q1 = float(data.get('q1', 0))
        q2 = float(data.get('q2', 0))
        r = float(data.get('r', 0))
        k = float(data.get('k', 8.99e9))
        
        results = {}
        
        if q1 and q2 and r and r != 0:
            results['F'] = k * abs(q1 * q2) / (r**2)
            results['E'] = k * abs(q1) / (r**2)
            results['V'] = k * q1 / r
        
        save_to_history('Electrostatics', data, results)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== SCIENTIFIC CALCULATOR ====================
@app.route('/api/calculator', methods=['POST'])
def calculator():
    try:
        data = request.json
        expression = data.get('expression', '0')
        
        results = {}
        
        try:
            # Replace math functions for safe evaluation
            safe_expr = expression
            safe_expr = safe_expr.replace('sin', f'sin')
            safe_expr = safe_expr.replace('cos', f'cos')
            safe_expr = safe_expr.replace('tan', f'tan')
            safe_expr = safe_expr.replace('sqrt', f'sqrt')
            safe_expr = safe_expr.replace('π', str(math.pi))
            safe_expr = safe_expr.replace('e', str(math.e))
            
            result = eval(safe_expr, {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'sqrt': math.sqrt,
                '__builtins__': {}
            })
            
            results['result'] = result
            save_to_history('Scientific Calculator', {'expression': expression}, results)
            return jsonify({'success': True, 'data': results})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== UNIT CONVERTER ====================
@app.route('/api/converter', methods=['POST'])
def converter():
    try:
        data = request.json
        conv_type = data.get('type', 'speed')
        value = float(data.get('value', 0))
        from_unit = data.get('from_unit', '')
        to_unit = data.get('to_unit', '')
        
        results = {}
        
        try:
            if conv_type == 'speed':
                result = UnitConverter.convert_speed(value, from_unit, to_unit)
            elif conv_type == 'mass':
                result = UnitConverter.convert_mass(value, from_unit, to_unit)
            elif conv_type == 'distance':
                result = UnitConverter.convert_distance(value, from_unit, to_unit)
            elif conv_type == 'energy':
                result = UnitConverter.convert_energy(value, from_unit, to_unit)
            elif conv_type == 'voltage':
                result = UnitConverter.convert_voltage(value, from_unit, to_unit)
            else:
                result = 0
            
            results['result'] = result
            results['from'] = f"{value} {from_unit}"
            results['to'] = f"{result} {to_unit}"
            save_to_history('Unit Converter', data, results)
            return jsonify({'success': True, 'data': results})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== HISTORY ====================
@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(load_history())

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    HISTORY_FILE.write_text('[]')
    return jsonify({'status': 'cleared'})

# ==================== PAGE ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/module/<module_name>')
def module_page(module_name):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
