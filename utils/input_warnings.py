"""
Input Validation with Real-time Warnings
Provides warnings for unrealistic physics values
"""


class InputValidator:
    """Validates physics inputs and provides warnings"""
    
    @staticmethod
    def validate_kinematics(u, v, a, t, s):
        """Validate kinematics inputs and return warnings"""
        warnings = []
        
        # Check for unrealistic velocities (>300 m/s ≈ 670 mph)
        if u is not None and abs(u) > 300:
            warnings.append("⚠ Initial velocity is very high (>300 m/s). Check for errors?")
        if v is not None and abs(v) > 300:
            warnings.append("⚠ Final velocity is very high (>300 m/s). Check for errors?")
        
        # Check for unrealistic acceleration (>100 m/s²)
        if a is not None and abs(a) > 100:
            warnings.append("⚠ Acceleration is very high (>100 m/s²). Check for errors?")
        
        # Check for unrealistic time (>1000 seconds)
        if t is not None and t > 1000:
            warnings.append("⚠ Time is very large (>1000s). Check for errors?")
        
        # Check for unrealistic displacement (>1 million meters)
        if s is not None and abs(s) > 1000000:
            warnings.append("⚠ Displacement is very large (>1M meters). Check for errors?")
        
        # Physics consistency checks
        if u is not None and v is not None and a is not None and t is not None:
            # v = u + at
            expected_v = u + a * t
            if abs(v - expected_v) > 1:
                warnings.append("⚠ Values may be inconsistent with kinematics equations")
        
        return warnings
    
    @staticmethod
    def validate_ohms_law(V, I, R):
        """Validate Ohm's Law inputs and return warnings"""
        warnings = []
        
        # Check for unrealistic voltage (>1000V is industrial)
        if V is not None and V > 1000:
            warnings.append("⚠ Voltage is very high (>1000V). This is industrial level.")
        
        # Check for unrealistic current (>100A is heavy industrial)
        if I is not None and I > 100:
            warnings.append("⚠ Current is very high (>100A). This is industrial level.")
        
        # Check for unrealistic resistance (<0.001Ω or >1MΩ)
        if R is not None and R < 0.001:
            warnings.append("⚠ Resistance is very low (<0.001Ω). Check for errors?")
        if R is not None and R > 1000000:
            warnings.append("⚠ Resistance is very high (>1MΩ). Check for errors?")
        
        # Physics consistency checks
        if V is not None and I is not None and R is not None:
            expected_V = I * R
            if abs(V - expected_V) > 0.1:
                warnings.append("⚠ Values may not satisfy Ohm's Law (V = I·R)")
        
        return warnings
    
    @staticmethod
    def validate_energy(m, v, KE):
        """Validate Energy inputs and return warnings"""
        warnings = []
        
        # Check for unrealistic mass (>1000000 kg = 1000 ton)
        if m is not None and m > 1000000:
            warnings.append("⚠ Mass is very large (>1M kg). Check for errors?")
        
        # Check for unrealistic velocity (>300 m/s)
        if v is not None and abs(v) > 300:
            warnings.append("⚠ Velocity is very high (>300 m/s). Check for errors?")
        
        # Physics consistency checks
        if m is not None and v is not None and KE is not None:
            expected_KE = 0.5 * m * v * v
            if abs(KE - expected_KE) > 1:
                warnings.append("⚠ Values may not satisfy KE = ½mv²")
        
        return warnings
    
    @staticmethod
    def validate_momentum(m1, v1, m2, v2):
        """Validate Momentum inputs and return warnings"""
        warnings = []
        
        # Check for unrealistic masses
        if m1 is not None and m1 > 1000000:
            warnings.append("⚠ Object 1 mass is very large (>1M kg). Check for errors?")
        if m2 is not None and m2 > 1000000:
            warnings.append("⚠ Object 2 mass is very large (>1M kg). Check for errors?")
        
        # Check for unrealistic velocities
        if v1 is not None and abs(v1) > 300:
            warnings.append("⚠ Object 1 velocity is very high (>300 m/s). Check for errors?")
        if v2 is not None and abs(v2) > 300:
            warnings.append("⚠ Object 2 velocity is very high (>300 m/s). Check for errors?")
        
        # Check for reasonable collision scenario
        if v1 is not None and v2 is not None:
            if (v1 > 0 and v2 > 0 and v1 <= v2):
                warnings.append("ℹ Same direction: Object 1 slower. They may not collide.")
        
        return warnings
    
    @staticmethod
    def validate_optics(f, u, v):
        """Validate Optics inputs and return warnings"""
        warnings = []
        
        # Check for focal length at zero (undefined)
        if f is not None and f == 0:
            warnings.append("⚠ Focal length cannot be zero!")
        
        # Check for very large focal length (>1000 cm)
        if f is not None and abs(f) > 1000:
            warnings.append("⚠ Focal length is very large (>1000 cm). Check for errors?")
        
        # Check for object distance <= focal length (special cases)
        if f is not None and u is not None:
            if abs(u) <= abs(f):
                warnings.append("ℹ Object is at or inside focal point. Virtual image will form.")
        
        # Check for very large distances
        if u is not None and u > 10000:
            warnings.append("⚠ Object distance is very large (>10km). Check for errors?")
        if v is not None and v > 10000:
            warnings.append("⚠ Image distance is very large (>10km). Check for errors?")
        
        return warnings
    
    @staticmethod
    def get_warning_message(warnings):
        """Format warnings into a display message"""
        if not warnings:
            return None
        
        message = "⚠ WARNINGS:\n"
        for warning in warnings[:3]:  # Limit to 3 warnings
            message += f"• {warning}\n"
        
        if len(warnings) > 3:
            message += f"• ...and {len(warnings) - 3} more warning(s)"
        
        return message
