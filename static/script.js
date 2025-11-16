// Physics Lab - Web App JavaScript

// ==================== STATE & UTILITIES ====================
let history = [];
let currentModule = 'home';
let calcExpression = '0';
let sidebarCollapsed = false;

// Theme Management
document.getElementById('themeToggle').addEventListener('click', toggleTheme);

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
}

// Sidebar Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarCollapsed = !sidebarCollapsed;
    sidebar.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
}

// Load saved theme and sidebar state
window.addEventListener('load', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
    }
    
    const savedSidebarState = localStorage.getItem('sidebarCollapsed');
    if (savedSidebarState === 'true') {
        sidebarCollapsed = true;
        document.getElementById('sidebar').classList.add('collapsed');
    }
    
    loadModule('home');
    loadHistory();
});

// ==================== MODULE NAVIGATION ====================
function loadModule(moduleName) {
    // Hide all modules
    document.querySelectorAll('.module-view').forEach(el => {
        el.style.display = 'none';
    });
    
    // Show selected module
    const module = document.getElementById(moduleName);
    if (module) {
        module.style.display = 'block';
        currentModule = moduleName;
        console.log('Loaded module:', moduleName);
    } else {
        console.warn('Module not found:', moduleName);
    }
    
    // Update active button
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
}

// ==================== CALCULATION FUNCTIONS ====================
async function calculate(module) {
    let inputs = {};
    let endpoint = '';
    
    switch(module) {
        case 'kinematics':
            inputs = {
                u: parseFloat(document.getElementById('kin_u').value) || 0,
                a: parseFloat(document.getElementById('kin_a').value) || 0,
                t: parseFloat(document.getElementById('kin_t').value) || 0,
                s: parseFloat(document.getElementById('kin_s').value) || 0,
                v: parseFloat(document.getElementById('kin_v').value) || 0
            };
            endpoint = '/api/kinematics';
            break;
        case 'ohms':
            inputs = {
                V: parseFloat(document.getElementById('ohm_V').value) || 0,
                I: parseFloat(document.getElementById('ohm_I').value) || 0,
                R: parseFloat(document.getElementById('ohm_R').value) || 0
            };
            endpoint = '/api/ohms-law';
            break;
        case 'energy':
            inputs = {
                m: parseFloat(document.getElementById('ener_m').value) || 0,
                v: parseFloat(document.getElementById('ener_v').value) || 0,
                h: parseFloat(document.getElementById('ener_h').value) || 0,
                g: parseFloat(document.getElementById('ener_g').value) || 9.8
            };
            endpoint = '/api/energy';
            break;
        case 'momentum':
            inputs = {
                m1: parseFloat(document.getElementById('mom_m1').value) || 0,
                v1: parseFloat(document.getElementById('mom_v1').value) || 0,
                m2: parseFloat(document.getElementById('mom_m2').value) || 0,
                v2: parseFloat(document.getElementById('mom_v2').value) || 0
            };
            endpoint = '/api/momentum';
            break;
        case 'optics':
            inputs = {
                f: parseFloat(document.getElementById('opt_f').value) || 0,
                u: parseFloat(document.getElementById('opt_u').value) || 0,
                v: parseFloat(document.getElementById('opt_v').value) || 0
            };
            endpoint = '/api/optics';
            break;
        case 'thermo':
            inputs = {
                m: parseFloat(document.getElementById('therm_m').value) || 0,
                c: parseFloat(document.getElementById('therm_c').value) || 0,
                delta_t: parseFloat(document.getElementById('therm_dt').value) || 0
            };
            endpoint = '/api/thermodynamics';
            break;
        case 'circular':
            inputs = {
                m: parseFloat(document.getElementById('circ_m').value) || 0,
                v: parseFloat(document.getElementById('circ_v').value) || 0,
                r: parseFloat(document.getElementById('circ_r').value) || 0,
                omega: parseFloat(document.getElementById('circ_omega').value) || 0
            };
            endpoint = '/api/circular-motion';
            break;
        case 'projectile':
            inputs = {
                v0: parseFloat(document.getElementById('proj_v0').value) || 0,
                theta: parseFloat(document.getElementById('proj_theta').value) || 45,
                g: parseFloat(document.getElementById('proj_g').value) || 9.8
            };
            endpoint = '/api/projectile-motion';
            break;
        case 'shm':
            inputs = {
                m: parseFloat(document.getElementById('shm_m').value) || 0,
                k: parseFloat(document.getElementById('shm_k').value) || 0,
                A: parseFloat(document.getElementById('shm_A').value) || 0
            };
            endpoint = '/api/shm';
            break;
        case 'electrostatics':
            inputs = {
                q1: parseFloat(document.getElementById('elec_q1').value) || 0,
                q2: parseFloat(document.getElementById('elec_q2').value) || 0,
                r: parseFloat(document.getElementById('elec_r').value) || 0
            };
            endpoint = '/api/electrostatics';
            break;
    }
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputs)
        });
        
        const response_data = await response.json();
        
        // Extract data from new response format
        const results = response_data.success ? response_data.data : response_data;
        
        if (!response_data.success && response_data.error) {
            alert('Calculation error: ' + response_data.error);
            return;
        }
        
        displayResults(module, results);
        loadHistory();
    } catch (error) {
        console.error('Error:', error);
        alert('Calculation error: ' + error.message);
    }
}

function displayResults(module, results) {
    // Map module names to result div prefixes
    const prefixMap = {
        'kinematics': 'kin',
        'ohms': 'ohm',
        'energy': 'ener',
        'momentum': 'mom',
        'optics': 'opt',
        'thermo': 'therm',
        'circular': 'circ',
        'projectile': 'proj',
        'shm': 'shm',
        'electrostatics': 'elec',
        'calculator': 'calc'
    };
    
    const modulePrefix = prefixMap[module];
    const resultsDiv = document.getElementById(`${modulePrefix}_results`);
    
    if (!resultsDiv) {
        console.warn('Results div not found for module:', module, 'prefix:', modulePrefix);
        return;
    }
    
    let html = '<h3>✓ Results</h3>';
    for (const [key, value] of Object.entries(results)) {
        if (key !== 'error' && key !== 'success' && key !== 'data') {
            const displayKey = formatKey(key);
            const displayValue = typeof value === 'number' ? value.toFixed(4) : value;
            html += `<div class="result-item">
                        <div class="result-label">${displayKey}</div>
                        <div class="result-value">${displayValue}</div>
                    </div>`;
        }
    }
    resultsDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Generate graphs based on module
    const inputs = getInputsForModule(module);
    generateGraph(module, results, inputs);
}

function getInputsForModule(module) {
    switch(module) {
        case 'kinematics':
            return {
                u: parseFloat(document.getElementById('kin_u').value) || 0,
                a: parseFloat(document.getElementById('kin_a').value) || 0,
                t: parseFloat(document.getElementById('kin_t').value) || 0
            };
        case 'ohms':
            return {
                V: parseFloat(document.getElementById('ohm_V').value) || 0,
                I: parseFloat(document.getElementById('ohm_I').value) || 0,
                R: parseFloat(document.getElementById('ohm_R').value) || 0
            };
        case 'energy':
            return {
                m: parseFloat(document.getElementById('ener_m').value) || 0,
                v: parseFloat(document.getElementById('ener_v').value) || 0,
                h: parseFloat(document.getElementById('ener_h').value) || 0,
                g: parseFloat(document.getElementById('ener_g').value) || 9.8
            };
        case 'projectile':
            return {
                v0: parseFloat(document.getElementById('proj_v0').value) || 0,
                theta: parseFloat(document.getElementById('proj_theta').value) || 45,
                g: parseFloat(document.getElementById('proj_g').value) || 9.8
            };
        case 'circular':
            return {
                m: parseFloat(document.getElementById('circ_m').value) || 0,
                v: parseFloat(document.getElementById('circ_v').value) || 0,
                r: parseFloat(document.getElementById('circ_r').value) || 0
            };
        case 'shm':
            return {
                m: parseFloat(document.getElementById('shm_m').value) || 0,
                k: parseFloat(document.getElementById('shm_k').value) || 0,
                A: parseFloat(document.getElementById('shm_A').value) || 0
            };
        case 'momentum':
            return {
                m1: parseFloat(document.getElementById('mom_m1').value) || 0,
                v1: parseFloat(document.getElementById('mom_v1').value) || 0,
                m2: parseFloat(document.getElementById('mom_m2').value) || 0,
                v2: parseFloat(document.getElementById('mom_v2').value) || 0
            };
        case 'optics':
            return {
                f: parseFloat(document.getElementById('opt_f').value) || 0,
                u: parseFloat(document.getElementById('opt_u').value) || 0,
                v: parseFloat(document.getElementById('opt_v').value) || 0
            };
        case 'thermo':
            return {
                m: parseFloat(document.getElementById('therm_m').value) || 0,
                c: parseFloat(document.getElementById('therm_c').value) || 0,
                delta_t: parseFloat(document.getElementById('therm_dt').value) || 0
            };
        case 'electrostatics':
            return {
                q1: parseFloat(document.getElementById('elec_q1').value) || 0,
                q2: parseFloat(document.getElementById('elec_q2').value) || 0,
                r: parseFloat(document.getElementById('elec_r').value) || 0
            };
        default:
            return {};
    }
}

function generateGraph(module, results, inputs) {
    // Map module names to graph div prefixes
    const prefixMap = {
        'kinematics': 'kin',
        'ohms': 'ohm',
        'energy': 'ener',
        'momentum': 'mom',
        'optics': 'opt',
        'thermo': 'therm',
        'circular': 'circ',
        'projectile': 'proj',
        'shm': 'shm',
        'electrostatics': 'elec'
    };
    
    const modulePrefix = prefixMap[module];
    const graphDiv = document.getElementById(`${modulePrefix}_graph`);
    
    if (!graphDiv) {
        console.warn('Graph div not found for module:', module, 'prefix:', modulePrefix);
        return;
    }
    
    let data = [];
    let layout = {
        title: `${module.charAt(0).toUpperCase() + module.slice(1)} Analysis`,
        xaxis: { title: 'Variable' },
        yaxis: { title: 'Value' },
        plot_bgcolor: '#1a1a1a',
        paper_bgcolor: '#0f0f0f',
        font: { color: '#ffffff' },
        margin: { l: 60, r: 40, t: 60, b: 60 }
    };
    
    switch(module) {
        case 'kinematics':
            if (inputs.t > 0) {
                const times = Array.from({length: 50}, (_, i) => i * inputs.t / 50);
                const velocities = times.map(t => inputs.u + inputs.a * t);
                const displacements = times.map(t => inputs.u * t + 0.5 * inputs.a * t * t);
                
                data = [
                    { x: times, y: velocities, name: 'Velocity', type: 'scatter', mode: 'lines', line: { color: '#90caf9', width: 3 } },
                    { x: times, y: displacements, name: 'Displacement', type: 'scatter', mode: 'lines', line: { color: '#ff9800', width: 3 }, yaxis: 'y2' }
                ];
                layout.yaxis2 = { title: 'Displacement (m)', overlaying: 'y', side: 'right' };
            }
            layout.xaxis.title = 'Time (s)';
            layout.yaxis.title = 'Velocity (m/s)';
            break;
            
        case 'ohms':
            if (inputs.R > 0) {
                const currents = Array.from({length: 50}, (_, i) => i * 10 / 50);
                const voltages = currents.map(I => I * inputs.R);
                const powers = currents.map(I => I * I * inputs.R);
                
                data = [
                    { x: currents, y: voltages, name: 'V-I Characteristic', type: 'scatter', mode: 'lines', line: { color: '#64b5f6', width: 3 } },
                    { x: currents, y: powers, name: 'Power', type: 'scatter', mode: 'lines', line: { color: '#ef5350', width: 3 }, yaxis: 'y2' }
                ];
                layout.yaxis2 = { title: 'Power (W)', overlaying: 'y', side: 'right' };
            }
            layout.xaxis.title = 'Current (A)';
            layout.yaxis.title = 'Voltage (V)';
            break;
            
        case 'energy':
            if (inputs.m > 0 && inputs.h > 0) {
                const heights = Array.from({length: 50}, (_, i) => i * inputs.h / 50);
                const velocities = Array.from({length: 50}, (_, i) => i * 20 / 50);
                const PE = heights.map(h => inputs.m * inputs.g * h);
                const KE = velocities.map(v => 0.5 * inputs.m * v * v);
                
                data = [
                    { x: heights, y: PE, name: 'Potential Energy', type: 'scatter', mode: 'lines', line: { color: '#81c784', width: 3 } },
                    { x: velocities, y: KE, name: 'Kinetic Energy', type: 'scatter', mode: 'lines', line: { color: '#ff7043', width: 3 } }
                ];
                layout.xaxis.title = 'Height / Velocity';
                layout.yaxis.title = 'Energy (J)';
            }
            break;
            
        case 'projectile':
            if (inputs.v0 > 0 && inputs.theta >= 0) {
                const theta_rad = inputs.theta * Math.PI / 180;
                const t_flight = 2 * inputs.v0 * Math.sin(theta_rad) / inputs.g;
                const times = Array.from({length: 100}, (_, i) => i * t_flight / 100);
                const x = times.map(t => inputs.v0 * Math.cos(theta_rad) * t);
                const y = times.map(t => inputs.v0 * Math.sin(theta_rad) * t - 0.5 * inputs.g * t * t);
                
                data = [
                    { x: x, y: y, name: 'Trajectory', type: 'scatter', mode: 'lines+markers', line: { color: '#64b5f6', width: 3 }, marker: { size: 4 } }
                ];
                layout.xaxis.title = 'Horizontal Distance (m)';
                layout.yaxis.title = 'Height (m)';
                layout.title = 'Projectile Trajectory';
            }
            break;
            
        case 'circular':
            if (inputs.v > 0 && inputs.r > 0) {
                const angles = Array.from({length: 100}, (_, i) => i * 2 * Math.PI / 100);
                const x = angles.map(a => inputs.r * Math.cos(a));
                const y = angles.map(a => inputs.r * Math.sin(a));
                
                data = [
                    { x: x, y: y, name: 'Circular Path', type: 'scatter', mode: 'lines', line: { color: '#ba68c8', width: 2 } },
                    { x: [0], y: [0], name: 'Center', type: 'scatter', mode: 'markers', marker: { size: 8, color: '#ff9800' } }
                ];
                layout.xaxis.title = 'X (m)';
                layout.yaxis.title = 'Y (m)';
                layout.title = 'Circular Motion Path';
            }
            break;
            
        case 'shm':
            if (inputs.m > 0 && inputs.k > 0 && inputs.A > 0) {
                const omega = Math.sqrt(inputs.k / inputs.m);
                const period = 2 * Math.PI / omega;
                const times = Array.from({length: 200}, (_, i) => i * 3 * period / 200);
                const displacement = times.map(t => inputs.A * Math.sin(omega * t));
                const velocity = times.map(t => inputs.A * omega * Math.cos(omega * t));
                
                data = [
                    { x: times, y: displacement, name: 'Displacement', type: 'scatter', mode: 'lines', line: { color: '#29b6f6', width: 3 } },
                    { x: times, y: velocity, name: 'Velocity', type: 'scatter', mode: 'lines', line: { color: '#ffa726', width: 3 }, yaxis: 'y2' }
                ];
                layout.yaxis2 = { title: 'Velocity (m/s)', overlaying: 'y', side: 'right' };
                layout.title = 'Simple Harmonic Motion';
            }
            layout.xaxis.title = 'Time (s)';
            layout.yaxis.title = 'Displacement (m)';
            break;
            
        case 'momentum':
            if (inputs.m1 > 0 && inputs.v1 > 0) {
                const masses = Array.from({length: 50}, (_, i) => (i + 1) * inputs.m1 / 50);
                const momenta = masses.map(m => m * inputs.v1);
                
                data = [
                    { x: masses, y: momenta, name: 'Momentum', type: 'scatter', mode: 'lines', line: { color: '#4dd0e1', width: 3 } }
                ];
                layout.xaxis.title = 'Mass (kg)';
                layout.yaxis.title = 'Momentum (kg·m/s)';
                layout.title = 'Momentum Analysis';
            }
            break;
            
        case 'optics':
            if (inputs.f > 0 && inputs.u > inputs.f) {
                const distances = Array.from({length: 50}, (_, i) => (i + 1) * inputs.u / 50);
                const imageDistances = distances.map(u => (inputs.f * u) / (u - inputs.f));
                const magnifications = distances.map((u, idx) => -(imageDistances[idx] / u));
                
                data = [
                    { x: distances, y: imageDistances, name: 'Image Distance', type: 'scatter', mode: 'lines', line: { color: '#4dd0e1', width: 3 } },
                    { x: distances, y: magnifications, name: 'Magnification', type: 'scatter', mode: 'lines', line: { color: '#ffb74d', width: 3 }, yaxis: 'y2' }
                ];
                layout.yaxis2 = { title: 'Magnification', overlaying: 'y', side: 'right' };
                layout.xaxis.title = 'Object Distance (m)';
                layout.yaxis.title = 'Image Distance (m)';
                layout.title = 'Optics Analysis';
            }
            break;
            
        case 'thermo':
            if (inputs.m > 0 && inputs.c > 0) {
                const tempChanges = Array.from({length: 50}, (_, i) => i * (inputs.delta_t > 0 ? inputs.delta_t : 100) / 50);
                const heat = tempChanges.map(dt => inputs.m * inputs.c * dt);
                
                data = [
                    { x: tempChanges, y: heat, name: 'Heat Energy', type: 'scatter', mode: 'lines', line: { color: '#ef5350', width: 3 } }
                ];
                layout.xaxis.title = 'Temperature Change (°C)';
                layout.yaxis.title = 'Heat Energy (J)';
                layout.title = 'Thermodynamics Analysis';
            }
            break;
            
        case 'electrostatics':
            if (inputs.q1 !== 0 && inputs.q2 !== 0 && inputs.r > 0) {
                const distances = Array.from({length: 50}, (_, i) => (i + 1) * inputs.r / 50);
                const k = 8.99e9;
                const forces = distances.map(r => Math.abs((k * inputs.q1 * inputs.q2) / (r * r)));
                
                data = [
                    { x: distances, y: forces, name: 'Coulomb Force', type: 'scatter', mode: 'lines', line: { color: '#ce93d8', width: 3 } }
                ];
                layout.xaxis.title = 'Distance (m)';
                layout.yaxis.title = 'Force (N)';
                layout.title = 'Electrostatics Analysis';
            }
            break;
    }
    
    if (data.length > 0) {
        graphDiv.style.display = 'block';
        Plotly.newPlot(graphDiv, data, layout, { responsive: true });
    }
}

function formatKey(key) {
    const keyMap = {
        'v': 'Final Velocity (v)',
        's': 'Displacement (s)',
        't': 'Time (t)',
        'V': 'Voltage (V)',
        'I': 'Current (I)',
        'R': 'Resistance (R)',
        'P': 'Power (P)',
        'KE': 'Kinetic Energy (KE)',
        'PE': 'Potential Energy (PE)',
        'ME': 'Mechanical Energy (ME)',
        'p1': 'Momentum 1',
        'p2': 'Momentum 2',
        'p_total': 'Total Momentum',
        'm': 'Magnification',
        'u': 'Object Distance',
        'v': 'Image Distance',
        'f': 'Focal Length',
        'Q': 'Heat (Q)',
        'F_c': 'Centripetal Force',
        'a_c': 'Centripetal Acceleration',
        'omega': 'Angular Velocity',
        'max_height': 'Max Height',
        'range': 'Range',
        'time_of_flight': 'Time of Flight',
        'T': 'Period',
        'f': 'Frequency',
        'E': 'Energy',
        'max_v': 'Max Velocity',
        'F': 'Force',
        'result': 'Result'
    };
    return keyMap[key] || key;
}

// ==================== CALCULATOR FUNCTIONS ====================
function appendCalc(value) {
    if (calcExpression === '0' && value !== '.') {
        calcExpression = value;
    } else {
        calcExpression += value;
    }
    updateCalcDisplay();
}

function updateCalcDisplay() {
    document.getElementById('calc_display').value = calcExpression;
}

function clearCalc() {
    calcExpression = '0';
    updateCalcDisplay();
}

async function calculateCalc() {
    try {
        const response = await fetch('/api/calculator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression: calcExpression })
        });
        
        const results = await response.json();
        if (results.result !== undefined) {
            calcExpression = results.result.toString();
            updateCalcDisplay();
        } else if (results.error) {
            alert('Error: ' + results.error);
        }
    } catch (error) {
        alert('Calculation error: ' + error.message);
    }
}

// ==================== HISTORY ====================
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        history = await response.json();
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function showHistory() {
    const modal = document.getElementById('historyModal');
    const content = document.getElementById('historyContent');
    
    if (history.length === 0) {
        content.innerHTML = '<p>No calculations yet.</p>';
    } else {
        let html = '';
        for (const calc of history.slice().reverse()) {
            html += `<div class="formula-item">
                        <h4>[${calc.timestamp}] ${calc.module}</h4>
                        <p><strong>Inputs:</strong> ${JSON.stringify(calc.inputs)}</p>
                        <p><strong>Results:</strong> ${JSON.stringify(calc.outputs)}</p>
                    </div>`;
        }
        content.innerHTML = html;
    }
    
    modal.classList.remove('hidden');
}

function showFormulas() {
    const modal = document.getElementById('formulasModal');
    const content = document.getElementById('formulasContent');
    
    const formulas = {
        'Kinematics': [
            'v = u + at',
            's = ut + ½at²',
            'v² = u² + 2as',
            's = (u + v)t / 2'
        ],
        'Ohm\'s Law': [
            'V = IR',
            'P = VI',
            'P = I²R'
        ],
        'Energy': [
            'KE = ½mv²',
            'PE = mgh',
            'E = KE + PE'
        ],
        'Momentum': [
            'p = mv',
            'F = Δp/Δt',
            'p_total = p₁ + p₂'
        ],
        'Optics': [
            '1/f = 1/u + 1/v',
            'm = -v/u',
            'f = R/2'
        ],
        'Thermodynamics': [
            'Q = mcΔT',
            'ΔE = Q - W',
            'PV = nRT'
        ],
        'Circular Motion': [
            'v = ωr',
            'F_c = mv²/r',
            'T = 2π/ω'
        ],
        'Projectile Motion': [
            'x = v₀cos(θ)t',
            'y = v₀sin(θ)t - ½gt²',
            'R = v₀²sin(2θ)/g'
        ],
        'SHM': [
            'x = A sin(ωt + φ)',
            'v = Aω cos(ωt + φ)',
            'T = 2π√(m/k)'
        ],
        'Electrostatics': [
            'F = k|q₁q₂|/r²',
            'E = kQ/r²',
            'V = kQ/r'
        ]
    };
    
    let html = '';
    for (const [category, items] of Object.entries(formulas)) {
        html += `<div class="formula-item">
                    <h4>${category}</h4>`;
        for (const formula of items) {
            html += `<p>${formula}</p>`;
        }
        html += `</div>`;
    }
    
    content.innerHTML = html;
    modal.classList.remove('hidden');
}

async function clearHistory() {
    if (confirm('Clear all calculation history?')) {
        try {
            await fetch('/api/history/clear', { method: 'POST' });
            history = [];
            alert('History cleared!');
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    }
}

// ==================== MODAL FUNCTIONS ====================
function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.add('hidden');
    }
});

// ==================== UNIT CONVERTER ====================
const unitSystems = {
    speed: ['m/s', 'km/h', 'mph', 'ft/s', 'knots'],
    mass: ['kg', 'g', 'mg', 'lb', 'oz'],
    distance: ['m', 'cm', 'mm', 'km', 'ft', 'in', 'mile'],
    energy: ['J', 'kJ', 'MJ', 'cal', 'kcal', 'eV', 'Wh'],
    voltage: ['V', 'kV', 'mV', 'μV']
};

function updateConverterUnits() {
    const type = document.getElementById('conv_type').value;
    const units = unitSystems[type];
    
    const fromSelect = document.getElementById('conv_from');
    const toSelect = document.getElementById('conv_to');
    
    fromSelect.innerHTML = units.map(u => `<option value="${u}">${u}</option>`).join('');
    toSelect.innerHTML = units.map(u => `<option value="${u}">${u}</option>`).join('');
    
    if (units.length > 1) {
        toSelect.value = units[1];
    }
}

async function convertUnits() {
    const type = document.getElementById('conv_type').value;
    const value = parseFloat(document.getElementById('conv_value').value) || 0;
    const fromUnit = document.getElementById('conv_from').value;
    const toUnit = document.getElementById('conv_to').value;
    
    if (value === 0 || !fromUnit || !toUnit) {
        alert('Please enter a value and select units');
        return;
    }
    
    try {
        const response = await fetch('/api/converter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type, value, from_unit: fromUnit, to_unit: toUnit })
        });
        
        const result = await response.json();
        
        const resultsDiv = document.getElementById('conv_results');
        resultsDiv.innerHTML = `
            <h3>✓ Result</h3>
            <div class="result-item">
                <div class="result-label">${value} ${fromUnit}</div>
                <div class="result-value">=</div>
                <div class="result-label">${result.result.toFixed(6)} ${toUnit}</div>
            </div>
        `;
        resultsDiv.style.display = 'block';
    } catch (error) {
        console.error('Conversion error:', error);
        alert('Conversion error: ' + error.message);
    }
}

// Initialize converter on page load
window.addEventListener('load', () => {
    updateConverterUnits();
});
