# ⚛️ Physics Lab - A Simple Physics Calculator

A beginner-friendly web app for doing physics calculations! It's got 8 different physics calculators and some cool graphs to visualize what's happening.

## What Can You Do With It?

- **Calculate physics stuff** - kinematics, energy, momentum, electricity, vectors, projectile motion, and circular motion
- **See graphs** - Every calculation makes an interactive graph
- **View your history** - See all the calculations you've done
- **Dark/Light mode** - Pick whatever you like
- **Works on phones too** - It's responsive!

## How to Run It

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your computer.

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
Go to `http://localhost:5000` and you're done!

## The Physics Calculators

1. **Kinematics** - Calculate motion (velocity, acceleration, distance)
2. **Freefall** - Objects falling with gravity
3. **Work & Energy** - Kinetic energy, potential energy, work
4. **Momentum** - Conservation of momentum
5. **Electricity** - Ohm's law and Coulomb's law
6. **Vectors** - Vector math and operations
7. **Projectile Motion** - Calculate how stuff flies through the air
8. **Circular Motion** - Objects moving in circles

## Project Files

```
physics-app/
├── web_app.py              # The backend (Python)
├── requirements.txt        # What you need to install
├── templates/
│   └── index.html          # The website
├── static/
│   ├── script.js           # Makes it work
│   └── style.css           # Makes it look nice
└── modules/                # All the physics calculators
    ├── kinematics.py
    ├── freefall_dynamics.py
    ├── work_energy.py
    ├── momentum.py
    ├── electricity.py
    ├── vectors.py
    ├── projectile_motion.py
    └── circular_motion.py
```

## How It Works

1. You pick a calculator from the side menu
2. Type in your numbers
3. Click "Calculate"
4. See the answer and a graph
5. Your calculation gets saved in history

## Issues?

**Can't see the icons?**
- Refresh your browser

**Calculations not working?**
- Make sure you entered valid numbers
- Check the browser console for errors (press F12)

**App won't start?**
- Check if Python is installed: `python --version`
- Make sure port 5000 isn't being used
- Try installing requirements again: `pip install -r requirements.txt`

## Want to Deploy It?

You can put this on the internet for free using Vercel:

1. Push your code to GitHub
2. Go to https://vercel.com
3. Connect your GitHub account
4. Select this project
5. Click "Deploy"

Done! It's live on the internet now!

## Made with

- Python + Flask (the backend)
- HTML + CSS + JavaScript (the website)
- Plotly (the graphs)

## License

MIT - Do whatever you want with it!
