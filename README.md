<div align="center">

# 🧪 Physics Calculator

**A comprehensive, interactive web-based physics calculator with real-time graphing, dark mode, and responsive design**

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=flat-square&logo=vercel)](https://vercel.com)

[Live Demo](#-live-demo) • [Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📸 Overview

Physics Calculator is a modern, feature-rich web application designed for students, educators, and physics enthusiasts. It combines intuitive UI/UX with powerful calculation engines, supporting 11 physics modules, a scientific calculator, and a universal unit converter.

**Key Highlights:**
- ⚡ Real-time calculations with instant visual feedback
- 📊 Interactive Plotly.js graphs for all modules
- 🌓 Dark/Light theme with persistent preferences
- 📱 Fully responsive - optimized for desktop, tablet, and mobile
- 🎨 Modern, clean design with smooth animations
- 💾 Calculation history tracking
- 🔄 Unit converter with 5 conversion types

---

## 🚀 Features

### 🔬 Physics Modules (11 Total)

| Module | Calculations | Features |
|--------|--------------|----------|
| **Kinematics** | Velocity, displacement, acceleration | Interactive trajectory graphs |
| **Ohm's Law** | Voltage, current, resistance, power | V-I characteristic curves |
| **Energy** | Kinetic, potential, mechanical energy | Energy comparison charts |
| **Momentum** | Linear momentum, impulse, collisions | Momentum conservation |
| **Optics** | Focal length, magnification, lens power | Optical system analysis |
| **Thermodynamics** | Heat, work, internal energy | Process visualization |
| **Circular Motion** | Centripetal force, angular velocity | Orbital path plots |
| **Projectile Motion** | Range, height, time of flight | Trajectory simulation |
| **Simple Harmonic Motion** | Displacement, velocity, energy | Oscillation graphs |
| **Electrostatics** | Electric field, force, potential | Field visualization |
| **Scientific Calculator** | 40+ operations (sin, cos, log, etc.) | Full calculator interface |

### 🎯 Core Features

- ✅ **Real-time Calculations** - Instant results as you type
- ✅ **Interactive Graphs** - Plotly.js visualization for all modules
- ✅ **Unit Converter** - Speed, mass, distance, energy, voltage
- ✅ **Dark/Light Theme** - Persistent theme preferences
- ✅ **Responsive Design** - 6 responsive breakpoints
- ✅ **Mobile Optimized** - Collapsible sidebar, touch-friendly
- ✅ **History Tracking** - View past calculations
- ✅ **Calculation Display** - Show all formulas and steps
- ✅ **Input Validation** - Smart error checking

---

## 💻 Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0.0
- Werkzeug 3.0.1
- RESTful API architecture

**Frontend:**
- HTML5 (semantic markup)
- CSS3 (custom properties, Grid, Flexbox)
- JavaScript ES6+ (vanilla, no frameworks)
- Plotly.js 2.26.0 (interactive charts)

**Deployment:**
- Vercel (serverless Python support)
- GitHub (version control)

---

## 🎯 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/physics-calculator.git
cd physics-calculator

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
python web_app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

The app will be running and ready to use! 🎉

---

## 🌐 Live Demo

**Deployed on Vercel:** [https://physics-calculator.vercel.app](https://physics-calculator.vercel.app)

Try it now - no installation required!

---

## 📁 Project Structure

```
physics-calculator/
│
├── 📄 web_app.py                 # Flask backend (API endpoints)
├── 📄 requirements.txt            # Python dependencies
├── 📄 vercel.json                 # Vercel deployment config
│
├── 📁 templates/
│   └── index.html                 # Main HTML interface (457 lines)
│
├── 📁 static/
│   ├── style.css                  # Responsive styling (1141 lines)
│   └── script.js                  # Client-side logic (755 lines)
│
├── 📁 modules/                    # Physics calculation modules
│   ├── kinematics.py
│   ├── ohms_law.py
│   ├── energy.py
│   ├── momentum.py
│   ├── optics.py
│   ├── thermodynamics.py
│   ├── circular_motion.py
│   ├── projectile_motion.py
│   ├── simple_harmonic_motion.py
│   ├── electrostatics.py
│   └── scientific_calculator.py
│
└── 📁 utils/                      # Utility functions
    ├── validators.py              # Input validation
    ├── unit_converter.py           # Unit conversions
    ├── history.py                  # History management
    ├── tooltips.py                 # Help tooltips
    └── plotter.py                  # Graph utilities
```

---

## 🔌 API Endpoints

All endpoints accept POST requests with JSON payloads and return JSON responses.

### Physics Calculations

```
POST /api/kinematics              # Kinematics calculations
POST /api/ohms_law                # Ohm's Law (V=IR, P=VI)
POST /api/energy                  # Energy (KE, PE, ME)
POST /api/momentum                # Momentum calculations
POST /api/optics                  # Optical system calculations
POST /api/thermodynamics          # Thermodynamic processes
POST /api/circular_motion         # Circular motion analysis
POST /api/projectile_motion       # Projectile trajectory
POST /api/simple_harmonic_motion  # SHM analysis
POST /api/electrostatics          # Electrostatic calculations
```

### Utilities

```
POST /api/converter               # Unit conversion
POST /api/history                 # Get/save calculation history
```

### Example Request

```bash
curl -X POST http://localhost:5000/api/kinematics \
  -H "Content-Type: application/json" \
  -d '{
    "u": 10,
    "a": 2,
    "t": 5
  }'
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Select a Module** - Click any physics module in the sidebar
2. **Enter Values** - Input your parameters in the input fields
3. **Calculate** - Click the "Calculate" button
4. **View Results** - See instant calculations and graphs
5. **Export** - Save graphs or view calculation history

### Example: Kinematics

```
Initial Velocity (u): 5 m/s
Acceleration (a): 2 m/s²
Time (t): 10 s

Results:
✓ Final Velocity (v): 25 m/s
✓ Displacement (s): 150 m
✓ Graph: Interactive velocity/displacement plot
```

### Keyboard Shortcuts

- `Enter` - Calculate (when focused on input)
- `Esc` - Close modals
- `D` - Toggle dark mode
- `M` - Toggle mobile menu

---

## 🎨 Design Features

### Responsive Breakpoints

- **280px+** - Extra small phones
- **360px+** - Small phones
- **481px+** - Mobile devices
- **769px+** - Tablets
- **1024px+** - Small desktops
- **1920px+** - Large displays

### Theme System

- ✨ **Dark Mode** - Easy on the eyes
- ☀️ **Light Mode** - High contrast
- 💾 **Persistent** - Theme preference saved

### Accessibility

- 🎯 WCAG 2.1 compliant
- 🎨 High contrast ratios
- ⌨️ Full keyboard navigation
- 📱 Mobile-friendly touch targets

---

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Import in Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Click "Deploy"

3. **Done!** Your app is live in minutes

The `vercel.json` is pre-configured for optimal Flask deployment.

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Set up Flask web app
3. Reload app
4. Visit your domain

---

## 🐛 Troubleshooting

**Graph not showing?**
- Clear browser cache (Ctrl+Shift+Del)
- Check console for JavaScript errors (F12)
- Ensure Plotly.js CDN is accessible

**Calculations returning errors?**
- Verify input values are valid numbers
- Check units are correct
- Review server logs: `python web_app.py`

**Mobile layout broken?**
- Update browser to latest version
- Check viewport meta tag in HTML
- Try different browser

**Server won't start?**
- Ensure Port 5000 is available
- Check Python version: `python --version`
- Install dependencies: `pip install -r requirements.txt`

---

## 📊 Performance

- ⚡ **Fast Calculations** - Results in <100ms
- 📦 **Lightweight** - CSS: 35KB, JS: 25KB
- 🎯 **Optimized** - Minified production assets
- 🔄 **Caching** - Browser caching enabled

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Guidelines
- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Test thoroughly before submitting

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify the code
- ✅ Distribute
- ✅ Use privately

---

## 💡 Roadmap

- [ ] Export calculations to PDF
- [ ] Batch calculations
- [ ] Custom unit definitions
- [ ] Error propagation analysis
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced graphing options
- [ ] API documentation (Swagger)

---

## 📞 Support & Contact

- **Issues** - [GitHub Issues](https://github.com/yourusername/physics-calculator/issues)
- **Discussions** - [GitHub Discussions](https://github.com/yourusername/physics-calculator/discussions)
- **Email** - your.email@example.com

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Plotly](https://plotly.com/) - Interactive charts
- [Vercel](https://vercel.com) - Hosting platform
- Physics textbooks and educational resources

---

<div align="center">

**Made with ❤️ by [Your Name]**

⭐ If this project helps you, please consider giving it a star!

[⬆ Back to top](#-physics-calculator)

</div>
