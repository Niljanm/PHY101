# API Documentation

Complete reference for Physics Calculator REST API endpoints and usage examples.

## Base URL

```
http://localhost:5000  (local development)
https://physics-calculator.vercel.app  (production)
```

## Authentication

Currently, all endpoints are public. No authentication required.

## Response Format

All responses are in JSON format with the following structure:

### Success Response

```json
{
  "success": true,
  "data": {
    "result1": 123.45,
    "result2": 67.89,
    "unit": "m/s"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Invalid input values"
}
```

---

## Physics Modules

### 1. Kinematics

Calculate motion parameters using kinematic equations.

**Endpoint**: `POST /api/kinematics`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `u` | float | Initial velocity (m/s) | Optional |
| `v` | float | Final velocity (m/s) | Optional |
| `a` | float | Acceleration (m/s²) | Optional |
| `t` | float | Time (s) | Optional |
| `s` | float | Displacement (m) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/kinematics \
  -H "Content-Type: application/json" \
  -d '{
    "u": 10,
    "a": 5,
    "t": 3
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "v": 25,
    "s": 52.5,
    "unit": "m/s, m"
  }
}
```

**Formulas**:
- Final velocity: `v = u + at`
- Displacement: `s = ut + 0.5*a*t²`
- Final velocity squared: `v² = u² + 2as`

---

### 2. Ohm's Law

Calculate electrical parameters using Ohm's Law.

**Endpoint**: `POST /api/ohms_law`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `V` | float | Voltage (V) | Optional |
| `I` | float | Current (A) | Optional |
| `R` | float | Resistance (Ω) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/ohms_law \
  -H "Content-Type: application/json" \
  -d '{
    "V": 12,
    "I": 2
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "R": 6,
    "P": 24,
    "unit": "Ω, W"
  }
}
```

**Formulas**:
- Resistance: `R = V / I`
- Current: `I = V / R`
- Power: `P = V * I`

---

### 3. Energy

Calculate energy in different forms.

**Endpoint**: `POST /api/energy`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `m` | float | Mass (kg) | Yes |
| `v` | float | Velocity (m/s) | Optional |
| `h` | float | Height (m) | Optional |
| `g` | float | Gravitational acceleration (m/s²) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/energy \
  -H "Content-Type: application/json" \
  -d '{
    "m": 5,
    "v": 10,
    "h": 20,
    "g": 9.8
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "KE": 250,
    "PE": 980,
    "ME": 1230,
    "unit": "J"
  }
}
```

**Formulas**:
- Kinetic Energy: `KE = 0.5 * m * v²`
- Potential Energy: `PE = m * g * h`
- Mechanical Energy: `ME = KE + PE`

---

### 4. Momentum

Calculate momentum and related quantities.

**Endpoint**: `POST /api/momentum`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `m` | float | Mass (kg) | Yes |
| `v` | float | Velocity (m/s) | Yes |
| `F` | float | Force (N) | Optional |
| `t` | float | Time (s) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/momentum \
  -H "Content-Type: application/json" \
  -d '{
    "m": 2,
    "v": 15
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "p": 30,
    "unit": "kg*m/s"
  }
}
```

**Formulas**:
- Momentum: `p = m * v`
- Impulse: `J = F * t = Δp`

---

### 5. Optics

Calculate optical system parameters.

**Endpoint**: `POST /api/optics`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `f` | float | Focal length (cm) | Optional |
| `u` | float | Object distance (cm) | Optional |
| `v` | float | Image distance (cm) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/optics \
  -H "Content-Type: application/json" \
  -d '{
    "f": 10,
    "u": 30
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "v": 15,
    "m": -0.5,
    "unit": "cm"
  }
}
```

**Formulas**:
- Lens formula: `1/f = 1/u + 1/v`
- Magnification: `m = -v/u`

---

### 6. Thermodynamics

Calculate thermodynamic processes.

**Endpoint**: `POST /api/thermodynamics`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `Q` | float | Heat (J) | Optional |
| `W` | float | Work (J) | Optional |
| `U` | float | Internal energy (J) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/thermodynamics \
  -H "Content-Type: application/json" \
  -d '{
    "Q": 1000,
    "W": 300
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "U": 700,
    "unit": "J"
  }
}
```

**Formulas**:
- First Law: `ΔU = Q - W`
- Heat: `Q = n * Cp * ΔT`

---

### 7. Circular Motion

Calculate circular motion parameters.

**Endpoint**: `POST /api/circular_motion`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `m` | float | Mass (kg) | Yes |
| `v` | float | Velocity (m/s) | Yes |
| `r` | float | Radius (m) | Yes |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/circular_motion \
  -H "Content-Type: application/json" \
  -d '{
    "m": 2,
    "v": 10,
    "r": 5
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "ac": 20,
    "Fc": 40,
    "unit": "m/s², N"
  }
}
```

**Formulas**:
- Centripetal acceleration: `ac = v²/r`
- Centripetal force: `Fc = m*v²/r`
- Angular velocity: `ω = v/r`

---

### 8. Projectile Motion

Calculate projectile trajectory parameters.

**Endpoint**: `POST /api/projectile_motion`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `u` | float | Initial velocity (m/s) | Yes |
| `θ` | float | Launch angle (degrees) | Yes |
| `g` | float | Gravitational acceleration (m/s²) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/projectile_motion \
  -H "Content-Type: application/json" \
  -d '{
    "u": 50,
    "θ": 45
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "R": 254.96,
    "H": 63.74,
    "T": 7.22,
    "unit": "m, s"
  }
}
```

**Formulas**:
- Range: `R = u²*sin(2θ)/g`
- Max Height: `H = u²*sin²(θ)/(2g)`
- Time of Flight: `T = 2*u*sin(θ)/g`

---

### 9. Simple Harmonic Motion

Calculate SHM parameters.

**Endpoint**: `POST /api/simple_harmonic_motion`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `A` | float | Amplitude (m) | Optional |
| `f` | float | Frequency (Hz) | Optional |
| `T` | float | Period (s) | Optional |
| `t` | float | Time (s) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/simple_harmonic_motion \
  -H "Content-Type: application/json" \
  -d '{
    "A": 5,
    "f": 2
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "T": 0.5,
    "ω": 12.566,
    "E": 25,
    "unit": "s, rad/s, J"
  }
}
```

**Formulas**:
- Period: `T = 1/f`
- Angular frequency: `ω = 2π*f`
- Total energy: `E = 0.5*m*ω²*A²`

---

### 10. Electrostatics

Calculate electrostatic field and force parameters.

**Endpoint**: `POST /api/electrostatics`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `q1` | float | Charge 1 (C) | Optional |
| `q2` | float | Charge 2 (C) | Optional |
| `r` | float | Distance (m) | Optional |
| `E` | float | Electric field (N/C) | Optional |

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/electrostatics \
  -H "Content-Type: application/json" \
  -d '{
    "q1": 1e-6,
    "q2": 2e-6,
    "r": 0.5
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "F": 0.072,
    "V": 36000,
    "unit": "N, V"
  }
}
```

**Formulas**:
- Coulomb's Force: `F = k*q1*q2/r²` (k=8.99×10⁹)
- Electric Potential: `V = k*q/r`
- Electric Field: `E = F/q = k*Q/r²`

---

## Utility Endpoints

### Unit Converter

Convert between different units.

**Endpoint**: `POST /api/converter`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `conversion_type` | string | Type of conversion | Yes |
| `value` | float | Value to convert | Yes |
| `from_unit` | string | Source unit | Yes |
| `to_unit` | string | Target unit | Yes |

**Supported Conversions**:

```
- Speed: m/s, km/h, mph, knots
- Mass: kg, g, lb, oz
- Distance: m, km, cm, mm, inch, ft, mile
- Energy: J, kJ, cal, kcal, eV
- Voltage: V, mV, kV
```

**Request Example**:

```bash
curl -X POST http://localhost:5000/api/converter \
  -H "Content-Type: application/json" \
  -d '{
    "conversion_type": "speed",
    "value": 10,
    "from_unit": "m/s",
    "to_unit": "km/h"
  }'
```

**Response**:

```json
{
  "success": true,
  "data": {
    "result": 36,
    "unit": "km/h"
  }
}
```

---

### Calculation History

Get or save calculation history.

**Endpoint**: `POST /api/history`

**Parameters**:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `action` | string | "get" or "save" | Yes |
| `module` | string | Module name | If action="save" |
| `inputs` | object | Input values | If action="save" |
| `results` | object | Calculation results | If action="save" |

**Request Example (Get History)**:

```bash
curl -X POST http://localhost:5000/api/history \
  -H "Content-Type: application/json" \
  -d '{"action": "get"}'
```

**Response**:

```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2025-11-15 10:30:45",
      "module": "kinematics",
      "inputs": {"u": 10, "a": 5, "t": 3},
      "results": {"v": 25, "s": 52.5}
    }
  ]
}
```

---

## Error Handling

### Common Error Codes

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Invalid input values | Non-numeric input or missing required parameters |
| 400 | Parameters out of range | Negative where positive required |
| 404 | Endpoint not found | Invalid endpoint URL |
| 500 | Server error | Backend calculation error |

### Error Examples

**Example 1: Invalid Input**

```bash
curl -X POST http://localhost:5000/api/kinematics \
  -H "Content-Type: application/json" \
  -d '{"u": "invalid", "a": 5, "t": 3}'
```

Response:
```json
{
  "success": false,
  "error": "Invalid input values"
}
```

**Example 2: Missing Required Parameters**

```bash
curl -X POST http://localhost:5000/api/energy \
  -H "Content-Type: application/json" \
  -d '{"v": 10}'
```

Response:
```json
{
  "success": false,
  "error": "Mass is required for energy calculation"
}
```

---

## Rate Limiting

Currently no rate limiting is enforced. For production deployment, consider implementing:
- 100 requests per minute per IP
- Burst limit: 10 requests per second

---

## CORS

CORS is currently enabled for all origins. For production, configure:

```python
@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://yourdomain.com'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response
```

---

## Code Examples

### JavaScript Fetch

```javascript
async function calculate(module, data) {
  try {
    const response = await fetch(`/api/${module}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    
    if (result.success) {
      console.log('Results:', result.data);
    } else {
      console.error('Error:', result.error);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Usage
calculate('kinematics', { u: 10, a: 5, t: 3 });
```

### Python Requests

```python
import requests
import json

def calculate(module, data):
    url = f'http://localhost:5000/api/{module}'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, 
                               data=json.dumps(data),
                               headers=headers)
        result = response.json()
        
        if result['success']:
            print('Results:', result['data'])
        else:
            print('Error:', result['error'])
    except Exception as e:
        print('Request failed:', e)

# Usage
calculate('kinematics', {'u': 10, 'a': 5, 't': 3})
```

### cURL Examples

```bash
# Kinematics
curl -X POST http://localhost:5000/api/kinematics \
  -H "Content-Type: application/json" \
  -d '{"u": 10, "a": 5, "t": 3}'

# Energy
curl -X POST http://localhost:5000/api/energy \
  -H "Content-Type: application/json" \
  -d '{"m": 5, "v": 10, "h": 20}'

# Unit Conversion
curl -X POST http://localhost:5000/api/converter \
  -H "Content-Type: application/json" \
  -d '{"conversion_type": "speed", "value": 10, "from_unit": "m/s", "to_unit": "km/h"}'
```

---

## Versioning

Current API Version: **v1.0.0**

Future versions will be available at:
- `/api/v2/kinematics`
- `/api/v2/ohms_law`
- etc.

---

## Support

- **Bugs**: [GitHub Issues](https://github.com/yourusername/physics-calculator/issues)
- **Questions**: [GitHub Discussions](https://github.com/yourusername/physics-calculator/discussions)
- **Documentation**: [README.md](README.md)

---

**Last Updated**: November 15, 2025
