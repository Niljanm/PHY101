# Installation Guide

Complete step-by-step instructions for installing and running Physics Calculator on different platforms.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation on Windows](#installation-on-windows)
- [Installation on macOS](#installation-on-macos)
- [Installation on Linux](#installation-on-linux)
- [Docker Installation](#docker-installation)
- [Vercel Deployment](#vercel-deployment)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Disk Space**: 200 MB
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 2 GB
- **SSD**: 500 MB available space
- **Bandwidth**: 5 Mbps for CDN access

### Check Your Python Version

```bash
python --version
```

Should output: `Python 3.8.0` or higher

---

## Installation on Windows

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check ✅ "Add Python to PATH"
4. Click "Install Now"

**Verify Installation:**

```bash
python --version
pip --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/physics-calculator.git
cd physics-calculator
```

Or download as ZIP and extract.

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python web_app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 7: Open in Browser

Visit: **http://localhost:5000** 🎉

---

## Installation on macOS

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
brew install python@3.11
```

### Step 3: Verify Python Installation

```bash
python3 --version
```

### Step 4: Clone Repository

```bash
git clone https://github.com/yourusername/physics-calculator.git
cd physics-calculator
```

### Step 5: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 6: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 8: Run the Application

```bash
python web_app.py
```

### Step 9: Open in Browser

Visit: **http://localhost:5000**

### Optional: Create Alias (for easy startup)

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
alias physics-calc='cd ~/path/to/physics-calculator && source venv/bin/activate && python web_app.py'
```

Then use: `physics-calc`

---

## Installation on Linux

### Step 1: Update Package Manager

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade
```

**Fedora/RHEL:**
```bash
sudo dnf update
```

### Step 2: Install Python

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
```

### Step 3: Verify Installation

```bash
python3 --version
pip3 --version
```

### Step 4: Clone Repository

```bash
git clone https://github.com/yourusername/physics-calculator.git
cd physics-calculator
```

### Step 5: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 6: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 8: Run the Application

```bash
python web_app.py
```

### Step 9: Access Application

Visit: **http://localhost:5000**

### Optional: Run as Service

Create `/etc/systemd/system/physics-calc.service`:

```ini
[Unit]
Description=Physics Calculator
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/physics-calculator
ExecStart=/home/your_username/physics-calculator/venv/bin/python web_app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable physics-calc
sudo systemctl start physics-calc
sudo systemctl status physics-calc
```

---

## Docker Installation

### Prerequisites

- Docker installed ([docker.com](https://www.docker.com/))

### Step 1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=web_app.py

CMD ["python", "web_app.py"]
```

### Step 2: Create Docker Image

```bash
docker build -t physics-calculator .
```

### Step 3: Run Container

```bash
docker run -p 5000:5000 physics-calculator
```

### Step 4: Access Application

Visit: **http://localhost:5000**

### Optional: Use Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

Run:
```bash
docker-compose up
```

---

## Vercel Deployment

### Prerequisites

- GitHub account
- Vercel account ([vercel.com](https://vercel.com))

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Import in Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New..." → "Project"
3. Select "Import Git Repository"
4. Choose your physics-calculator repo
5. Click "Import"

### Step 3: Configure Project

- **Framework**: Other
- **Build Command**: Leave blank
- **Output Directory**: Leave blank
- **Root Directory**: ./

### Step 4: Deploy

Click "Deploy" and wait for completion (~2-3 minutes)

### Step 5: Access Live App

Your app will be available at:
```
https://physics-calculator-[random].vercel.app
```

---

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed

### Step 1: Login to Heroku

```bash
heroku login
```

### Step 2: Create App

```bash
heroku create your-app-name
```

### Step 3: Add Procfile

Create `Procfile`:

```
web: gunicorn web_app:app
```

Install gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 4: Deploy

```bash
git push heroku main
```

### Step 5: Access App

```bash
heroku open
```

---

## Troubleshooting

### Python Not Found

**Error**: `python: command not found`

**Solution**: 
- Check Python is installed: `python3 --version`
- Use `python3` instead of `python`
- Add Python to PATH (Windows)

### pip Not Found

**Error**: `pip: command not found`

**Solution**:
```bash
python -m pip --version
python -m pip install -r requirements.txt
```

### Port Already in Use

**Error**: `Address already in use :5000`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill -9 PID  # macOS/Linux
taskkill /PID PID /F  # Windows

# Or use different port
python web_app.py --port 8000
```

### Virtual Environment Issues

**Problem**: Virtual environment not activating

**Solution**:
```bash
# Delete and recreate
rm -rf venv  # or rmdir venv on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Dependencies Installation Fails

**Error**: `ERROR: Could not find a version that satisfies the requirement`

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### Flask Port Binding Error

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Check what's running on port 5000
sudo lsof -i :5000

# Change Flask port in web_app.py:
# app.run(debug=True, port=8000)
```

### Browser Shows "Cannot reach server"

**Solution**:
1. Verify Flask is running (check terminal output)
2. Check URL is exactly: `http://localhost:5000`
3. Try different browser
4. Check firewall settings
5. Restart Flask server

### Graphs Not Showing

**Error**: Calculations work but graphs are blank

**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check browser console (F12) for errors
3. Verify Plotly.js CDN is accessible
4. Try different browser

### Git Clone Permission Denied

**Error**: `Permission denied (publickey)`

**Solution**:
```bash
# Use HTTPS instead of SSH
git clone https://github.com/yourusername/physics-calculator.git

# Or generate SSH key:
ssh-keygen -t ed25519 -C "your_email@example.com"
```

---

## Next Steps

After successful installation:

1. **Explore Modules** - Try all 11 physics modules
2. **Read Documentation** - Check [README.md](README.md)
3. **Contribute** - See [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Deploy** - Use Vercel or Heroku
5. **Share** - Star the repo and share with friends!

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/physics-calculator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/physics-calculator/discussions)
- **Email**: your.email@example.com

---

**Happy calculating! 🚀**
