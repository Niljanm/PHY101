# ⚛️ Physics Lab - Master Core Physics Concepts

An interactive web application designed to help students understand and master fundamental physics through practical calculations and real-time visualizations.

## What Can You Do With It?

- **Calculate core physics** - Kinematics, Newton's Laws, Energy, and Momentum
- **Visualize instantly** - Every calculation generates interactive graphs
- **Track progress** - View your calculation history and compare results
- **Light/Dark mode** - Comfortable viewing in any lighting
- **Fully responsive** - Works perfectly on desktop, tablet, and mobile

## How to Run It

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Get the Code
```bash
git clone https://github.com/Niljanm/PHY101.git
cd PHY101
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
python web_app.py
```

### Step 5: Open in Browser
Go to `http://localhost:5000` and start learning!

## The 4 Core Modules

1. **Kinematics** - Analyze motion using equations of motion (velocity, acceleration, displacement)
2. **Newton's Laws** - Calculate forces and acceleration using Newton's fundamental laws
3. **PE & KE** - Understand energy transformations between potential and kinetic energy
4. **Momentum** - Explore momentum conservation and collisions

## Project Structure

```
PHY101/
├── web_app.py                 # Flask backend
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html             # Main interface
├── static/
│   ├── script.js              # JavaScript functionality
│   └── style.css              # Modern styling
└── modules/                   # Physics calculation modules
    ├── kinematics.py
    ├── momentum.py
    └── work_energy.py         # (PE & KE calculations)
```

## How It Works

1. Select a physics module from the sidebar
2. Input your values in the calculator
3. Click "Calculate" to see results
4. View the interactive graph visualization
5. Results automatically save to your history

## Features

- **Real-time Calculations** - Instant results as you input values
- **Interactive Graphs** - Beautiful visualizations using Plotly
- **Calculation History** - Track and reference all past calculations
- **Responsive Design** - Seamless experience across all devices
- **Dark/Light Themes** - Choose your preferred interface style
- **Educational Focus** - Perfect for students learning classical mechanics

## Troubleshooting

**Can't see anything?**
- Refresh your browser (Ctrl+R or Cmd+R)

**Calculations not working?**
- Ensure all inputs are valid numbers
- Check browser console (F12) for error messages

**App won't start?**
- Verify Python 3.8+ is installed: `python --version`
- Ensure port 5000 is available
- Reinstall dependencies: `pip install -r requirements.txt`

## Deploy It Online

Easily deploy to Vercel for free:

1. Push code to GitHub
2. Visit https://vercel.com
3. Import your repository
4. Click "Deploy"

## Built With

- **Backend**: Python + Flask
- **Frontend**: HTML + CSS + JavaScript
- **Visualizations**: Plotly
- **Design**: Modern UI with purple/violet theme

## License

MIT - Feel free to use and modify!

