# ⚛️ Physics Lab - Web Edition v2.0

A modern, responsive web-based physics calculator with 11 comprehensive modules, interactive visualizations, and automatic calculation history.

## Features

✨ **11 Physics Modules:**
- 📍 Kinematics - Motion equations
- ⚡ Ohm's Law - Electrical circuits
- ⚡ Energy - KE & PE calculations
- 💫 Momentum - Conservation & collisions
- 🔍 Optics - Lens & mirror systems
- 🌡️ Thermodynamics - Heat transfer
- 🔄 Circular Motion - Centripetal forces
- 🚀 Projectile Motion - Trajectory analysis
- 〰️ Simple Harmonic Motion - Oscillations
- ⚛️ Electrostatics - Coulomb's Law
- 🧮 Scientific Calculator - Advanced math

🎨 **Modern Design:**
- Responsive layout (desktop, tablet, mobile)
- Dark/Light theme toggle
- Smooth animations & transitions
- Intuitive sidebar navigation
- Professional color scheme

📊 **Powerful Features:**
- Real-time calculations
- Instant results display
- Full calculation history
- Formulas reference database
- Auto-save functionality
- Fast & lightweight

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Quick Start

1. **Navigate to project directory:**
```bash
cd Physics_app
```

2. **Install dependencies:**
```bash
pip install -r requirements_web.txt
```

3. **Run the web app:**
```bash
python web_app.py
```

4. **Open in browser:**
   - Navigate to `http://localhost:5000`
   - Bookmark for quick access

## Usage

### Running Calculations
1. Select a module from the left sidebar
2. Enter the known values
3. Click "Calculate" to get results
4. Results appear instantly below the form
5. History saves automatically

### Scientific Calculator
- Basic operations: +, -, ×, ÷
- Trigonometric: sin, cos, tan (in degrees)
- Powers & roots: x², √x, xⁿ
- Logarithms: ln, log₁₀
- Constants: π, e

### Features

**Theme Toggle:**
- Click the 🌙 icon in the top right
- Switch between dark/light modes
- Theme preference saved locally

**View History:**
- Click "History" in tools
- See all past calculations
- Module, timestamp, inputs, and results

**Formulas Reference:**
- Click "Formulas" to view equation library
- All physics formulas with descriptions
- Handy for quick reference

**Clear History:**
- Click "Clear" to remove all calculations
- Confirmation required

## Project Structure

```
Physics_app/
├── web_app.py              # Flask backend server
├── requirements_web.txt    # Python dependencies
├── templates/
│   └── index.html          # Main HTML interface
├── static/
│   ├── style.css           # Modern styling
│   └── script.js           # Frontend interactivity
├── data/
│   └── history.json        # Calculation history
└── README_WEB.md          # This file
```

## API Endpoints

### Calculations
- `POST /api/kinematics` - Motion equations
- `POST /api/ohms-law` - Electrical circuits
- `POST /api/energy` - Energy calculations
- `POST /api/momentum` - Momentum analysis
- `POST /api/optics` - Lens calculations
- `POST /api/thermodynamics` - Heat transfer
- `POST /api/circular-motion` - Circular motion
- `POST /api/projectile-motion` - Projectile trajectories
- `POST /api/shm` - Simple harmonic motion
- `POST /api/electrostatics` - Coulomb's Law
- `POST /api/calculator` - Scientific calculator

### History Management
- `GET /api/history` - Get all calculations
- `POST /api/history/clear` - Clear history

## Deployment

### Local Network
```bash
python web_app.py
# Access from other devices: http://<your-ip>:5000
```

### Cloud Deployment (Heroku, PythonAnywhere, etc.)

1. **Create Procfile:**
```
web: python web_app.py
```

2. **Set environment:**
```bash
export FLASK_ENV=production
```

3. **Deploy:**
   - Follow platform-specific instructions
   - Update data/history.json path if needed

## Browser Support

✓ Chrome/Edge (recommended)
✓ Firefox
✓ Safari
✓ Mobile browsers (iOS Safari, Chrome Android)

## Performance

- **Load Time:** < 1 second
- **Calculation Time:** < 10ms per request
- **File Size:** ~50KB (HTML+CSS+JS)
- **Memory Usage:** Minimal

## Keyboard Shortcuts

- `Escape` - Close modals
- `Enter` - Submit calculations (coming soon)
- `C` - Clear calculator (when in calculator mode)

## Tips & Tricks

1. **Batch Calculations:** Use history to compare multiple calculations
2. **Export Data:** Copy results directly from history view
3. **Mobile Friendly:** Works great on phones - bookmark the URL
4. **Offline Mode:** Works locally without internet (no external APIs)
5. **Multiple Instances:** Run on different ports: `python web_app.py --port 5001`

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python web_app.py
# Then access http://localhost:5001
```

### CSS/JS Not Loading
- Clear browser cache: `Ctrl+Shift+Delete`
- Hard refresh: `Ctrl+Shift+R`

### Calculations Not Working
- Check browser console: `F12` → Console
- Ensure Flask server is running
- Try refreshing the page

## Future Enhancements

- 📈 Real-time graph visualization
- 📱 Progressive Web App (PWA) support
- 🔒 User accounts & cloud sync
- 📤 Export calculations as PDF
- 🧑‍🏫 Physics tutorials & lessons
- 🌍 Multi-language support
- ⚙️ Custom unit definitions

## License

Free for personal & educational use

## Support

For issues or suggestions:
1. Check the Formulas section for equation reference
2. Review your input values for errors
3. Try clearing browser cache
4. Restart the Flask server

## Quick Start Commands

```bash
# Install dependencies
pip install flask werkzeug

# Run web app
python web_app.py

# Access at
http://localhost:5000
```

Enjoy exploring physics! ⚛️✨
