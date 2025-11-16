"""Projectile Motion Module"""
import math

class ProjectileMotion:
    @staticmethod
    def calculate(v0=0, theta=0, g=9.8):
        """Calculate projectile motion"""
        results = {}
        
        if v0 > 0 and theta >= 0 and theta <= 90:
            theta_rad = math.radians(theta)
            
            # Maximum height
            max_height = (v0 * v0 * math.sin(theta_rad) * math.sin(theta_rad)) / (2 * g)
            results['max_height'] = max_height
            
            # Time of flight
            time_of_flight = (2 * v0 * math.sin(theta_rad)) / g
            results['time_of_flight'] = time_of_flight
            
            # Range
            range_distance = (v0 * v0 * math.sin(2 * theta_rad)) / g
            results['range'] = range_distance
            
            # Time to max height
            time_to_max = (v0 * math.sin(theta_rad)) / g
            results['time_to_max_height'] = time_to_max
        
        return results
