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
    
    // On mobile, auto-close sidebar when navigating (handled by nav-btn click handlers)
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
            
        case 'ohms':
            if (inputs.R > 0) {
                const currents = Array.from({length: 50}, (_, i) => i * 10 / 50);
                const voltages = currents.map(I => I * inputs.R);
                const powers = currents.map(I => I * I * inputs.R);
                
                data = [
                    { x: currents, y: voltages, name: 'Voltage (V)', type: 'scatter', mode: 'lines', line: { color: '#64b5f6', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(100, 181, 246, 0.2)' },
                    { x: currents, y: powers, name: 'Power (W)', type: 'scatter', mode: 'lines', line: { color: '#ef5350', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(239, 83, 80, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Power (W)', overlaying: 'y', side: 'right', gridcolor: 'rgba(239, 83, 80, 0.2)' };
                layout.title += ` | Resistance: ${inputs.R.toFixed(2)} Ω`;
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
                const maxPE = inputs.m * inputs.g * inputs.h;
                const maxKE = 0.5 * inputs.m * 400;
                
                data = [
                    { x: heights, y: PE, name: 'Potential Energy (J)', type: 'scatter', mode: 'lines', line: { color: '#81c784', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(129, 199, 132, 0.2)' },
                    { x: velocities, y: KE, name: 'Kinetic Energy (J)', type: 'scatter', mode: 'lines', line: { color: '#ff7043', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(255, 112, 67, 0.2)' }
                ];
                layout.xaxis.title = 'Height (m) / Velocity (m/s)';
                layout.yaxis.title = 'Energy (J)';
                layout.title += ` | Max PE: ${maxPE.toFixed(2)} J | Max KE: ${maxKE.toFixed(2)} J`;
            }
            break;
            
        case 'projectile':
            if (inputs.v0 > 0 && inputs.theta >= 0) {
                const theta_rad = inputs.theta * Math.PI / 180;
                const t_flight = 2 * inputs.v0 * Math.sin(theta_rad) / inputs.g;
                const range = inputs.v0 * inputs.v0 * Math.sin(2 * theta_rad) / inputs.g;
                const maxHeight = (inputs.v0 * inputs.v0 * Math.sin(theta_rad) * Math.sin(theta_rad)) / (2 * inputs.g);
                const times = Array.from({length: 100}, (_, i) => i * t_flight / 100);
                const x = times.map(t => inputs.v0 * Math.cos(theta_rad) * t);
                const y = times.map(t => inputs.v0 * Math.sin(theta_rad) * t - 0.5 * inputs.g * t * t);
                
                data = [
                    { x: x, y: y, name: 'Trajectory', type: 'scatter', mode: 'lines+markers', line: { color: '#64b5f6', width: 3 }, marker: { size: 4 }, fill: 'tozeroy', fillcolor: 'rgba(100, 181, 246, 0.15)' },
                    { x: [range], y: [0], name: 'Landing Point', type: 'scatter', mode: 'markers', marker: { size: 10, color: '#ff5722', symbol: 'star' } }
                ];
                layout.xaxis.title = 'Horizontal Distance (m)';
                layout.yaxis.title = 'Height (m)';
                layout.title = `Projectile Trajectory | Range: ${range.toFixed(2)} m | Max Height: ${maxHeight.toFixed(2)} m`;
            }
            break;
            
        case 'circular':
            if (inputs.v > 0 && inputs.r > 0) {
                const angles = Array.from({length: 100}, (_, i) => i * 2 * Math.PI / 100);
                const x = angles.map(a => inputs.r * Math.cos(a));
                const y = angles.map(a => inputs.r * Math.sin(a));
                const period = 2 * Math.PI * inputs.r / inputs.v;
                const frequency = inputs.v / (2 * Math.PI * inputs.r);
                const centripetal = inputs.v * inputs.v / inputs.r;
                
                data = [
                    { x: x, y: y, name: 'Circular Path', type: 'scatter', mode: 'lines', line: { color: '#ba68c8', width: 3 }, fill: 'toself', fillcolor: 'rgba(186, 104, 200, 0.1)' },
                    { x: [0], y: [0], name: 'Center', type: 'scatter', mode: 'markers', marker: { size: 10, color: '#ff9800', symbol: 'diamond' } }
                ];
                layout.xaxis.title = 'X (m)';
                layout.yaxis.title = 'Y (m)';
                layout.title = `Circular Motion | Radius: ${inputs.r.toFixed(2)} m | Period: ${period.toFixed(3)} s | Centripetal Accel: ${centripetal.toFixed(2)} m/s²`;
                layout.xaxis.scaleanchor = 'y';
                layout.yaxis.scaleanchor = 'x';
            }
            break;
            
        case 'shm':
            if (inputs.m > 0 && inputs.k > 0 && inputs.A > 0) {
                const omega = Math.sqrt(inputs.k / inputs.m);
                const period = 2 * Math.PI / omega;
                const frequency = 1 / period;
                const times = Array.from({length: 200}, (_, i) => i * 3 * period / 200);
                const displacement = times.map(t => inputs.A * Math.sin(omega * t));
                const velocity = times.map(t => inputs.A * omega * Math.cos(omega * t));
                const maxVel = inputs.A * omega;
                
                data = [
                    { x: times, y: displacement, name: 'Displacement (m)', type: 'scatter', mode: 'lines', line: { color: '#29b6f6', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(41, 182, 246, 0.2)' },
                    { x: times, y: velocity, name: 'Velocity (m/s)', type: 'scatter', mode: 'lines', line: { color: '#ffa726', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(255, 167, 38, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Velocity (m/s)', overlaying: 'y', side: 'right', gridcolor: 'rgba(255, 167, 38, 0.2)' };
                layout.title = `Simple Harmonic Motion | Period: ${period.toFixed(3)} s | Frequency: ${frequency.toFixed(2)} Hz | Max Velocity: ${maxVel.toFixed(2)} m/s`;
            }
            layout.xaxis.title = 'Time (s)';
            layout.yaxis.title = 'Displacement (m)';
            break;
            
        case 'momentum':
            if (inputs.m1 > 0 && inputs.v1 > 0) {
                const masses = Array.from({length: 50}, (_, i) => (i + 1) * inputs.m1 / 50);
                const momenta = masses.map(m => m * inputs.v1);
                const totalMomentum = inputs.m1 * inputs.v1;
                
                data = [
                    { x: masses, y: momenta, name: 'Momentum (kg·m/s)', type: 'scatter', mode: 'lines+markers', line: { color: '#4dd0e1', width: 3 }, marker: { size: 5 }, fill: 'tozeroy', fillcolor: 'rgba(77, 208, 225, 0.2)' }
                ];
                layout.xaxis.title = 'Mass (kg)';
                layout.yaxis.title = 'Momentum (kg·m/s)';
                layout.title += ` | Total Momentum: ${totalMomentum.toFixed(2)} kg·m/s`;
            }
            break;
            
        case 'optics':
            if (inputs.f > 0 && inputs.u > inputs.f) {
                const distances = Array.from({length: 50}, (_, i) => (i + 1) * inputs.u / 50);
                const imageDistances = distances.map(u => (inputs.f * u) / (u - inputs.f));
                const magnifications = distances.map((u, idx) => -(imageDistances[idx] / u));
                
                data = [
                    { x: distances, y: imageDistances, name: 'Image Distance (m)', type: 'scatter', mode: 'lines', line: { color: '#4dd0e1', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(77, 208, 225, 0.2)' },
                    { x: distances, y: magnifications, name: 'Magnification', type: 'scatter', mode: 'lines', line: { color: '#ffb74d', width: 3 }, yaxis: 'y2', fill: 'tozeroy', fillcolor: 'rgba(255, 183, 77, 0.2)' }
                ];
                layout.yaxis2 = { title: 'Magnification', overlaying: 'y', side: 'right', gridcolor: 'rgba(255, 183, 77, 0.2)' };
                layout.xaxis.title = 'Object Distance (m)';
                layout.yaxis.title = 'Image Distance (m)';
                layout.title += ` | Focal Length: ${inputs.f.toFixed(2)} m`;
            }
            break;
            
        case 'thermo':
            if (inputs.m > 0 && inputs.c > 0) {
                const tempChanges = Array.from({length: 50}, (_, i) => i * (inputs.delta_t > 0 ? inputs.delta_t : 100) / 50);
                const heat = tempChanges.map(dt => inputs.m * inputs.c * dt);
                const totalHeat = inputs.m * inputs.c * (inputs.delta_t > 0 ? inputs.delta_t : 100);
                
                data = [
                    { x: tempChanges, y: heat, name: 'Heat Energy (J)', type: 'scatter', mode: 'lines+markers', line: { color: '#ef5350', width: 3 }, marker: { size: 5 }, fill: 'tozeroy', fillcolor: 'rgba(239, 83, 80, 0.2)' }
                ];
                layout.xaxis.title = 'Temperature Change (°C)';
                layout.yaxis.title = 'Heat Energy (J)';
                layout.title += ` | Specific Heat Capacity: ${inputs.c.toFixed(2)} J/(kg·°C) | Total Heat: ${totalHeat.toFixed(2)} J`;
            }
            break;
            
        case 'electrostatics':
            if (inputs.q1 !== 0 && inputs.q2 !== 0 && inputs.r > 0) {
                const distances = Array.from({length: 50}, (_, i) => (i + 1) * inputs.r / 50);
                const k = 8.99e9;
                const forces = distances.map(r => Math.abs((k * inputs.q1 * inputs.q2) / (r * r)));
                const forceAtR = Math.abs((k * inputs.q1 * inputs.q2) / (inputs.r * inputs.r));
                
                data = [
                    { x: distances, y: forces, name: 'Coulomb Force (N)', type: 'scatter', mode: 'lines', line: { color: '#ce93d8', width: 3 }, fill: 'tozeroy', fillcolor: 'rgba(206, 147, 216, 0.2)' }
                ];
                layout.xaxis.title = 'Distance (m)';
                layout.yaxis.title = 'Force (N)';
                layout.title += ` | Force @ ${inputs.r.toFixed(2)} m: ${forceAtR.toFixed(2)} N`;
            }
            break;
    }
    
    if (data.length > 0) {
        graphDiv.style.display = 'block';
        Plotly.newPlot(graphDiv, data, layout, { responsive: true, displayModeBar: true });
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
        
        if (!result.success || !result.data || result.data.result === undefined) {
            alert('Conversion failed: Invalid response from server');
            return;
        }
        
        const resultsDiv = document.getElementById('conv_results');
        resultsDiv.innerHTML = `
            <h3>✓ Result</h3>
            <div class="result-item">
                <div class="result-label">${value} ${fromUnit}</div>
                <div class="result-value">=</div>
                <div class="result-label">${result.data.result.toFixed(6)} ${toUnit}</div>
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
