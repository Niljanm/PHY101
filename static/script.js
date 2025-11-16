// Physics Lab - Web App JavaScript

// ==================== STATE & UTILITIES ====================
let history = [];
let currentModule = 'home';
let calcExpression = '0';
let sidebarCollapsed = false;

// Theme Management
function initializeThemeButtons() {
    const themeBtn1 = document.getElementById('themeToggle');
    const themeBtn2 = document.getElementById('themeToggle2');
    
    if (themeBtn1) {
        themeBtn1.addEventListener('click', toggleTheme);
    }
    if (themeBtn2) {
        themeBtn2.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    updateThemeButtons();
}

function updateThemeButtons() {
    const isDark = !document.body.classList.contains('light-mode');
    const themeBtn1 = document.getElementById('themeToggle');
    const themeBtn2 = document.getElementById('themeToggle2');
    
    if (themeBtn1) {
        themeBtn1.textContent = isDark ? '☀️' : '🌙';
    }
    if (themeBtn2) {
        themeBtn2.textContent = isDark ? '☀️' : '🌙';
    }
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
    initializeThemeButtons();
    updateThemeButtons();
    
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
    
    // Auto-close sidebar on mobile after selecting module
    if (window.innerWidth < 769) {
        const sidebar = document.getElementById('sidebar');
        if (!sidebar.classList.contains('collapsed')) {
            sidebar.classList.add('collapsed');
            sidebarCollapsed = true;
            localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
        }
    }
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
        case 'freefall':
            inputs = {
                h: parseFloat(document.getElementById('ff_h').value) || 0,
                v0: parseFloat(document.getElementById('ff_v0').value) || 0,
                t: parseFloat(document.getElementById('ff_t').value) || 0,
                g: parseFloat(document.getElementById('ff_g').value) || 9.8
            };
            endpoint = '/api/freefall';
            break;
        case 'work_energy':
            inputs = {
                force: parseFloat(document.getElementById('we_force').value) || 0,
                distance: parseFloat(document.getElementById('we_distance').value) || 0,
                mass: parseFloat(document.getElementById('we_mass').value) || 0,
                velocity: parseFloat(document.getElementById('we_velocity').value) || 0,
                height: parseFloat(document.getElementById('we_height').value) || 0,
                g: parseFloat(document.getElementById('we_g').value) || 9.8
            };
            endpoint = '/api/work_energy';
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
        case 'electricity':
            // Check which tab is active
            const ohmTab = document.getElementById('electricity_ohms_tab');
            if (ohmTab && ohmTab.classList.contains('active')) {
                inputs = {
                    type: 'ohms',
                    v: parseFloat(document.getElementById('elec_V').value) || 0,
                    i: parseFloat(document.getElementById('elec_I').value) || 0,
                    r: parseFloat(document.getElementById('elec_R').value) || 0
                };
            } else {
                inputs = {
                    type: 'coulombs',
                    q1: parseFloat(document.getElementById('elec_q1').value) || 0,
                    q2: parseFloat(document.getElementById('elec_q2').value) || 0,
                    r: parseFloat(document.getElementById('elec_r').value) || 0,
                    k: parseFloat(document.getElementById('elec_k').value) || 8.99e9
                };
            }
            endpoint = '/api/electricity';
            break;
        case 'vectors':
            // Check which tab is active
            const magTab = document.getElementById('vectors_magnitude_tab');
            const addTab = document.getElementById('vectors_addition_tab');
            const dotTab = document.getElementById('vectors_dot_tab');
            
            if (magTab && magTab.classList.contains('active')) {
                inputs = {
                    type: 'magnitude',
                    x: parseFloat(document.getElementById('vec_mag_x').value) || 0,
                    y: parseFloat(document.getElementById('vec_mag_y').value) || 0,
                    z: parseFloat(document.getElementById('vec_mag_z').value) || 0
                };
            } else if (addTab && addTab.classList.contains('active')) {
                inputs = {
                    type: 'addition',
                    x1: parseFloat(document.getElementById('vec_add_ax').value) || 0,
                    y1: parseFloat(document.getElementById('vec_add_ay').value) || 0,
                    x2: parseFloat(document.getElementById('vec_add_bx').value) || 0,
                    y2: parseFloat(document.getElementById('vec_add_by').value) || 0
                };
            } else if (dotTab && dotTab.classList.contains('active')) {
                inputs = {
                    type: 'dot',
                    x1: parseFloat(document.getElementById('vec_dot_ax').value) || 0,
                    y1: parseFloat(document.getElementById('vec_dot_ay').value) || 0,
                    x2: parseFloat(document.getElementById('vec_dot_bx').value) || 0,
                    y2: parseFloat(document.getElementById('vec_dot_by').value) || 0
                };
            } else {
                inputs = {
                    type: 'angle',
                    x1: parseFloat(document.getElementById('vec_angle_ax').value) || 0,
                    y1: parseFloat(document.getElementById('vec_angle_ay').value) || 0,
                    x2: parseFloat(document.getElementById('vec_angle_bx').value) || 0,
                    y2: parseFloat(document.getElementById('vec_angle_by').value) || 0
                };
            }
            endpoint = '/api/vectors';
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
        'freefall': 'ff',
        'work_energy': 'we',
        'momentum': 'mom',
        'electricity': 'elec',
        'vectors': 'vec'
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
        case 'freefall':
            return {
                h: parseFloat(document.getElementById('ff_h').value) || 0,
                v0: parseFloat(document.getElementById('ff_v0').value) || 0,
                t: parseFloat(document.getElementById('ff_t').value) || 0,
                g: parseFloat(document.getElementById('ff_g').value) || 9.8
            };
        case 'work_energy':
            return {
                mass: parseFloat(document.getElementById('we_mass').value) || 0,
                velocity: parseFloat(document.getElementById('we_velocity').value) || 0,
                height: parseFloat(document.getElementById('we_height').value) || 0,
                g: parseFloat(document.getElementById('we_g').value) || 9.8
            };
        case 'momentum':
            return {
                m1: parseFloat(document.getElementById('mom_m1').value) || 0,
                v1: parseFloat(document.getElementById('mom_v1').value) || 0,
                m2: parseFloat(document.getElementById('mom_m2').value) || 0,
                v2: parseFloat(document.getElementById('mom_v2').value) || 0
            };
        case 'electricity':
            return {
                v: parseFloat(document.getElementById('elec_V').value) || 0,
                i: parseFloat(document.getElementById('elec_I').value) || 0,
                r: parseFloat(document.getElementById('elec_R').value) || 0
            };
        case 'vectors':
            return {
                x: parseFloat(document.getElementById('vec_mag_x').value) || 0,
                y: parseFloat(document.getElementById('vec_mag_y').value) || 0,
                z: parseFloat(document.getElementById('vec_mag_z').value) || 0
            };
        default:
            return {};
    }
}

function generateGraph(module, results, inputs) {
    // Map module names to graph div prefixes
    const prefixMap = {
        'kinematics': 'kin',
        'freefall': 'ff',
        'work_energy': 'we',
        'momentum': 'mom',
        'electricity': 'elec',
        'vectors': 'vec'
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
        xaxis: { title: 'Variable', gridcolor: '#333333', showgrid: true },
        yaxis: { title: 'Value', gridcolor: '#333333', showgrid: true },
        plot_bgcolor: '#1a1a1a',
        paper_bgcolor: '#0f0f0f',
        font: { color: '#ffffff', family: 'Arial, sans-serif', size: 12 },
        margin: { l: 80, r: 80, t: 80, b: 70 },
        legend: { x: 0.02, y: 0.98, bgcolor: 'rgba(31, 31, 31, 0.8)', bordercolor: '#555', borderwidth: 1 },
        hovermode: 'x unified',
        showlegend: true
    };
    
    switch(module) {
        case 'kinematics':
            if (inputs.t > 0) {
                const times = Array.from({length: 50}, (_, i) => i * inputs.t / 50);
                const velocities = times.map(t => inputs.u + inputs.a * t);
                const displacements = times.map(t => inputs.u * t + 0.5 * inputs.a * t * t);
                const finalVel = inputs.u + inputs.a * inputs.t;
                const finalDisp = inputs.u * inputs.t + 0.5 * inputs.a * inputs.t * inputs.t;
                
                data = [
                    { x: times, y: velocities, name: 'Velocity (m/s)', type: 'scatter', mode: 'lines', line: { color: '#90caf9', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(144, 202, 249, 0.2)' },
                    { x: times, y: displacements, name: 'Displacement (m)', type: 'scatter', mode: 'lines', line: { color: '#ff9800', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(255, 152, 0, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Displacement (m)', overlaying: 'y', side: 'right', gridcolor: 'rgba(255, 152, 0, 0.2)' };
                layout.title += ` | Final Velocity: ${finalVel.toFixed(2)} m/s | Displacement: ${finalDisp.toFixed(2)} m`;
            }
            layout.xaxis.title = 'Time (s)';
            layout.yaxis.title = 'Velocity (m/s)';
            break;
            
        case 'freefall':
            if (inputs.t > 0) {
                const times = Array.from({length: 50}, (_, i) => i * inputs.t / 50);
                const velocities = times.map(t => inputs.v0 + inputs.g * t);
                const heights = times.map(t => inputs.v0 * t + 0.5 * inputs.g * t * t);
                
                data = [
                    { x: times, y: velocities, name: 'Velocity (m/s)', type: 'scatter', mode: 'lines', line: { color: '#90caf9', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(144, 202, 249, 0.2)' },
                    { x: times, y: heights, name: 'Height (m)', type: 'scatter', mode: 'lines', line: { color: '#4dd0e1', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(77, 208, 225, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Height (m)', overlaying: 'y', side: 'right' };
            }
            layout.xaxis.title = 'Time (s)';
            layout.yaxis.title = 'Velocity (m/s)';
            break;
            
        case 'work_energy':
            if (inputs.mass > 0 && inputs.height > 0) {
                const heights = Array.from({length: 50}, (_, i) => i * inputs.height / 50);
                const PE = heights.map(h => inputs.mass * inputs.g * h);
                const KE = Array.from({length: 50}, (_, i) => 0.5 * inputs.mass * Math.pow(inputs.velocity, 2) * i / 50);
                
                data = [
                    { x: heights, y: PE, name: 'Potential Energy (J)', type: 'scatter', mode: 'lines', line: { color: '#81c784', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(129, 199, 132, 0.2)' },
                    { x: Array.from({length: 50}, (_, i) => i * inputs.velocity / 50), y: KE, name: 'Kinetic Energy (J)', type: 'scatter', mode: 'lines', line: { color: '#ff7043', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(255, 112, 67, 0.2)' }
                ];
            }
            layout.xaxis.title = 'Parameter';
            layout.yaxis.title = 'Energy (J)';
            break;
            
        case 'momentum':
            if (inputs.m1 > 0 && inputs.v1 > 0) {
                const masses = Array.from({length: 50}, (_, i) => (i + 1) * inputs.m1 / 50);
                const momenta = masses.map(m => m * inputs.v1);
                const totalMomentum = inputs.m1 * inputs.v1;
                
                data = [
                    { x: masses, y: momenta, name: 'Momentum (kg·m/s)', type: 'scatter', mode: 'lines+markers', line: { color: '#4dd0e1', width: 3 }, marker: { size: 5 }, fill: 'tozeroy', fillcolor: 'rgba(77, 208, 225, 0.2)' }
                ];
                layout.title += ` | Total Momentum: ${totalMomentum.toFixed(2)} kg·m/s`;
            }
            layout.xaxis.title = 'Mass (kg)';
            layout.yaxis.title = 'Momentum (kg·m/s)';
            break;
            
        case 'electricity':
            if (inputs.r > 0) {
                const resistances = Array.from({length: 50}, (_, i) => (i + 1) * inputs.r / 50);
                const currents = resistances.map(R => inputs.v > 0 ? inputs.v / R : 0);
                const powers = resistances.map(R => inputs.v > 0 ? (inputs.v * inputs.v) / R : 0);
                
                data = [
                    { x: resistances, y: currents, name: 'Current (A)', type: 'scatter', mode: 'lines', line: { color: '#64b5f6', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(100, 181, 246, 0.2)' },
                    { x: resistances, y: powers, name: 'Power (W)', type: 'scatter', mode: 'lines', line: { color: '#ef5350', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(239, 83, 80, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Power (W)', overlaying: 'y', side: 'right' };
            }
            layout.xaxis.title = 'Resistance (Ω)';
            layout.yaxis.title = 'Current (A)';
            break;
            
        case 'vectors':
            const mag = Math.sqrt(inputs.x*inputs.x + inputs.y*inputs.y + inputs.z*inputs.z);
            data = [
                { x: [0, inputs.x], y: [0, inputs.y], name: 'Vector', type: 'scatter', mode: 'lines+markers', line: { color: '#90caf9', width: 3 }, marker: { size: 8 } }
            ];
            layout.title += ` | Magnitude: ${mag.toFixed(2)}`;
            layout.xaxis.title = 'X Component';
            layout.yaxis.title = 'Y Component';
            break;
    }
    
    if (data.length > 0) {
        graphDiv.style.display = 'block';
        Plotly.newPlot(graphDiv, data, layout, { responsive: true, displayModeBar: true });
    }
}

// Tab switching for modules with multiple calculation types
function switchTab(event, module, tabId) {
    event.preventDefault();
    
    // Hide all tabs for this module
    const tabs = document.querySelectorAll(`#${module} .tab-content`);
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Deactivate all buttons for this module
    const buttons = document.querySelectorAll(`#${module} .tab-btn`);
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab and activate button
    const selectedTab = document.getElementById(`${module}_${tabId}`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    event.target.classList.add('active');
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
        'result': 'Result',
        'magnitude': 'Magnitude',
        'resultant_x': 'Result X',
        'resultant_y': 'Result Y',
        'dot_product': 'Dot Product',
        'angle_degrees': 'Angle (°)',
        'angle_radians': 'Angle (rad)',
        'final_velocity': 'Final Velocity',
        'height': 'Height',
        'kinetic_energy': 'Kinetic Energy',
        'potential_energy': 'Potential Energy',
        'total_energy': 'Total Energy',
        'force': 'Force',
        'distance': 'Distance',
        'work': 'Work',
        'power': 'Power'
    };
    return keyMap[key] || key.replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2');
}

// ==================== HISTORY ====================
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        if (!response.ok) {
            console.error('Failed to load history:', response.status);
            history = [];
            return;
        }
        const data = await response.json();
        history = Array.isArray(data) ? data : [];
    } catch (error) {
        console.error('Error loading history:', error);
        history = [];
    }
}

function showHistory() {
    const modal = document.getElementById('historyModal');
    const content = document.getElementById('historyContent');
    
    if (!history || history.length === 0) {
        content.innerHTML = '<p>No calculations yet.</p>';
    } else {
        let html = '';
        const historyToShow = Array.isArray(history) ? history : [];
        for (const calc of historyToShow.slice().reverse()) {
            const timestamp = calc.timestamp || 'N/A';
            const module = calc.module || 'Unknown';
            const inputs = calc.inputs ? JSON.stringify(calc.inputs) : '{}';
            const outputs = calc.outputs ? JSON.stringify(calc.outputs) : '{}';
            html += `<div class="formula-item">
                        <h4>[${timestamp}] ${module}</h4>
                        <p><strong>Inputs:</strong> ${inputs}</p>
                        <p><strong>Results:</strong> ${outputs}</p>
                    </div>`;
        }
        content.innerHTML = html || '<p>No calculations yet.</p>';
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
        'Freefall Dynamics': [
            'h = v₀t + ½gt²',
            'v = v₀ + gt',
            'v² = v₀² + 2gh'
        ],
        'Work & Energy': [
            'Work = Force × Distance',
            'KE = ½mv²',
            'PE = mgh',
            'E = KE + PE'
        ],
        'Momentum': [
            'p = mv',
            'F = Δp/Δt',
            'p_total = p₁ + p₂'
        ],
        'Electricity': [
            'Ohm\'s Law: V = IR',
            'Power: P = VI',
            'Coulomb\'s Law: F = kq₁q₂/r²'
        ],
        'Vectors': [
            'Magnitude: |v| = √(x² + y² + z²)',
            'Addition: v_resultant = v₁ + v₂',
            'Dot Product: v₁ · v₂ = |v₁||v₂|cos(θ)'
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
