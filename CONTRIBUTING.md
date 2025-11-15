# Contributing to Physics Calculator

First off, thank you for considering contributing to Physics Calculator! It's people like you that make this tool such a great resource for physics education.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to maintainers.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the [issues list](https://github.com/yourusername/physics-calculator/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**How to Submit a Good Bug Report:**

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the observed behavior and what you expected instead
- Include screenshots/GIFs if possible
- Include your environment details:
  - OS and browser version
  - Python version
  - Flask version

**Example Bug Report:**

```markdown
Title: Kinematics calculator returns NaN for zero acceleration

Steps to Reproduce:
1. Go to Kinematics module
2. Enter u=5, a=0, t=10
3. Click Calculate

Expected: Show displacement and final velocity
Actual: Shows NaN error

Environment: Chrome 119, Windows 11, Python 3.11
```

### Suggesting Enhancements 💡

Enhancements include:
- New physics modules
- UI/UX improvements
- Performance optimizations
- Documentation updates

**How to Submit a Good Enhancement Suggestion:**

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Explain why this enhancement would be useful
- List some other physics calculator tools that have similar features

**Example Enhancement:**

```markdown
Title: Add Quantum Mechanics Module

Description:
Add a new module for basic quantum mechanics calculations including:
- Energy levels in atoms
- Wavelength/momentum relationships
- Uncertainty principle calculations

Why: Would benefit physics students learning quantum mechanics
```

### Pull Requests 🚀

- Fill in the required template
- Follow Python and JavaScript style guides (see below)
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

**Pull Request Process:**

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test thoroughly:
   ```bash
   python web_app.py
   ```
5. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a Pull Request with detailed description

---

## Development Setup

### Clone the Repository

```bash
git clone https://github.com/yourusername/physics-calculator.git
cd physics-calculator
```

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python web_app.py
```

Visit: `http://localhost:5000`

---

## Coding Guidelines

### Python Style (PEP 8)

```python
# Good
def calculate_displacement(initial_velocity, acceleration, time):
    """Calculate displacement using kinematic equation."""
    return initial_velocity * time + 0.5 * acceleration * time ** 2

# Bad
def calc_disp(u,a,t):
    return u*t+0.5*a*t**2
```

**Rules:**
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 88 characters
- Use meaningful variable names
- Add docstrings to functions
- Use type hints where applicable

### JavaScript Style (ES6+)

```javascript
// Good
function calculateKineticEnergy(mass, velocity) {
  if (mass <= 0 || velocity < 0) {
    console.error('Invalid input values');
    return null;
  }
  return 0.5 * mass * velocity ** 2;
}

// Bad
function calcKE(m,v){
  return 0.5*m*v*v;
}
```

**Rules:**
- Use `const` by default, `let` if reassignment needed, avoid `var`
- Use camelCase for variables and functions
- Use PascalCase for classes
- Add comments for complex logic
- Use arrow functions appropriately
- Proper error handling

### CSS Guidelines

```css
/* Good */
.button-primary {
  background-color: var(--primary-color);
  padding: 10px 20px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.button-primary:hover {
  transform: scale(1.05);
}

/* Bad */
.btn {
  background: blue;
  padding: 10px;
}
```

**Rules:**
- Use kebab-case for class names
- Use CSS custom properties (variables)
- Mobile-first approach
- 2 spaces for indentation
- Organize properties logically

---

## Adding a New Physics Module

### Step 1: Create Module File

Create `modules/new_module.py`:

```python
"""Module for calculating new physics concepts."""

def calculate_something(param1, param2):
    """
    Calculate something based on parameters.
    
    Args:
        param1 (float): First parameter
        param2 (float): Second parameter
    
    Returns:
        dict: Calculation results with keys like 'result1', 'result2'
    
    Raises:
        ValueError: If parameters are invalid
    """
    if param1 < 0 or param2 < 0:
        raise ValueError("Parameters must be non-negative")
    
    result1 = param1 + param2
    result2 = param1 * param2
    
    return {
        'result1': result1,
        'result2': result2,
        'unit': 'your_unit'
    }
```

### Step 2: Add API Endpoint

In `web_app.py`:

```python
@app.route('/api/new_module', methods=['POST'])
def new_module_api():
    """Handle new physics module calculations."""
    try:
        data = request.json
        param1 = float(data.get('param1', 0))
        param2 = float(data.get('param2', 0))
        
        from modules.new_module import calculate_something
        result = calculate_something(param1, param2)
        
        return jsonify({'success': True, 'data': result})
    except (ValueError, TypeError) as e:
        return jsonify({'success': False, 'error': str(e)})
```

### Step 3: Add HTML Interface

In `templates/index.html`:

```html
<!-- New Module Section -->
<div id="new-module" class="module-view hidden">
    <div class="input-group">
        <label for="param1">Parameter 1:</label>
        <input type="number" id="param1" placeholder="Enter value">
    </div>
    
    <div class="input-group">
        <label for="param2">Parameter 2:</label>
        <input type="number" id="param2" placeholder="Enter value">
    </div>
    
    <button class="btn-calculate" onclick="calculate('newModule')">
        Calculate
    </button>
    
    <div id="new-module-results" class="results hidden"></div>
    <div id="new-module-graph" class="graph hidden"></div>
</div>
```

### Step 4: Add JavaScript Function

In `static/script.js`:

```javascript
function calculateNewModule() {
  const param1 = parseFloat(document.getElementById('param1').value);
  const param2 = parseFloat(document.getElementById('param2').value);
  
  if (isNaN(param1) || isNaN(param2)) {
    alert('Please enter valid numbers');
    return;
  }
  
  fetch('/api/new_module', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ param1, param2 })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      displayResults('newModule', data.data);
      generateGraph('newModule', data.data, { param1, param2 });
    }
  });
}
```

### Step 5: Add Navigation Button

In `templates/index.html`, add to navigation:

```html
<button class="nav-btn" onclick="loadModule('newModule')" 
        data-emoji="🔬" title="New Module">
    New Module
</button>
```

---

## Testing

### Manual Testing

```bash
# Run the server
python web_app.py

# Test endpoints with curl
curl -X POST http://localhost:5000/api/kinematics \
  -H "Content-Type: application/json" \
  -d '{"u": 5, "a": 2, "t": 3}'
```

### Browser Testing

- Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- Test on mobile devices (portrait and landscape)
- Test with dark/light mode
- Check console for JavaScript errors (F12)

### Responsiveness Testing

Use browser DevTools:
1. Press F12
2. Click device toggle (Ctrl+Shift+M)
3. Test at different breakpoints:
   - 280px, 360px, 481px, 769px, 1024px, 1920px

---

## Documentation

### Docstring Format

```python
def function_name(param1, param2):
    """
    Short description of what the function does.
    
    Longer description if needed, explaining the logic
    and any important considerations.
    
    Args:
        param1 (type): Description
        param2 (type): Description
    
    Returns:
        type: Description of return value
    
    Raises:
        ExceptionType: When this exception occurs
    
    Examples:
        >>> result = function_name(10, 20)
        >>> result
        {'value': 200}
    """
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests

**Example:**

```
feat: Add wave optics module

- Add wave interference calculations
- Add diffraction pattern visualization
- Add API endpoint /api/wave-optics

Closes #123
```

---

## Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/physics-calculator/discussions)
- Check existing issues for similar topics
- Review the [README](README.md) documentation

---

## Recognition 🌟

Contributors will be recognized in:
- README.md acknowledgments section
- GitHub contributors page
- Release notes

Thank you for contributing to Physics Calculator! 🎉
