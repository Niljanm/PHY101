"""
Presets and Example Values
For helping users learn with pre-filled examples
"""

PRESETS = {
    "Kinematics": [
        {
            "name": "Free Fall",
            "description": "Object dropped from rest",
            "values": {"u": "0", "a": "9.8", "t": "5"}
        },
        {
            "name": "Car Acceleration",
            "description": "Car accelerating from rest",
            "values": {"u": "0", "a": "2.5", "t": "10"}
        },
        {
            "name": "Projectile Launch",
            "description": "Ball thrown upward",
            "values": {"u": "20", "a": "-9.8", "t": "2"}
        }
    ],
    "Ohms Law": [
        {
            "name": "Standard Circuit",
            "description": "Common household voltage",
            "values": {"V": "120", "R": "60"}
        },
        {
            "name": "LED Circuit",
            "description": "Low power LED",
            "values": {"V": "5", "R": "220"}
        },
        {
            "name": "Motor Circuit",
            "description": "Electric motor",
            "values": {"V": "12", "R": "8"}
        }
    ],
    "Energy": [
        {
            "name": "Running Person",
            "description": "Person running at 5 m/s",
            "values": {"m": "70", "v": "5"}
        },
        {
            "name": "Car",
            "description": "Car traveling at highway speed",
            "values": {"m": "1500", "v": "25"}
        },
        {
            "name": "Falling Object",
            "description": "Object dropped from 10m",
            "values": {"m": "5", "v": "14"}
        }
    ],
    "Momentum": [
        {
            "name": "Elastic Collision",
            "description": "Two objects colliding elastically",
            "values": {"m1": "2", "v1": "10", "m2": "3", "v2": "-5"}
        },
        {
            "name": "Inelastic Collision",
            "description": "Objects sticking together",
            "values": {"m1": "5", "v1": "8", "m2": "3", "v2": "0"}
        }
    ],
    "Optics": [
        {
            "name": "Converging Lens",
            "description": "Common magnifying glass",
            "values": {"f": "5", "u": "10"}
        },
        {
            "name": "Camera Lens",
            "description": "Typical camera focal length",
            "values": {"f": "50", "u": "500"}
        },
        {
            "name": "Microscope",
            "description": "High magnification lens",
            "values": {"f": "2", "u": "3"}
        }
    ]
}


def get_presets(module_name):
    """Get presets for a specific module"""
    return PRESETS.get(module_name, [])


def get_preset_values(module_name, preset_name):
    """Get specific preset values"""
    for preset in PRESETS.get(module_name, []):
        if preset["name"] == preset_name:
            return preset["values"]
    return None
