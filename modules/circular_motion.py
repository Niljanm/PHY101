"""Circular Motion Module"""
import math

class CircularMotion:
    @staticmethod
    def calculate(v=0, r=0, m=0, g=9.8):
        """Calculate circular motion"""
        results = {}
        
        if v > 0 and r > 0:
            # Angular velocity
            omega = v / r
            results['angular_velocity'] = omega
            
            # Period
            period = (2 * math.pi * r) / v
            results['period'] = period
            
            # Frequency
            frequency = v / (2 * math.pi * r)
            results['frequency'] = frequency
            
            # Centripetal acceleration
            centripetal_accel = (v * v) / r
            results['centripetal_acceleration'] = centripetal_accel
            
            # Centripetal force (if mass provided)
            if m > 0:
                centripetal_force = m * centripetal_accel
                results['centripetal_force'] = centripetal_force
        
        return results
