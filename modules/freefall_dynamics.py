"""Freefall Dynamics Module"""

class FreefallDynamics:
    @staticmethod
    def calculate_freefall(h=0, v0=0, t=0, g=9.8):
        """Calculate freefall motion"""
        results = {}
        
        if h > 0 and v0 == 0:
            # Height known, find time and final velocity
            t = (2 * h / g) ** 0.5
            v = g * t
            results['time'] = t
            results['final_velocity'] = v
            results['height'] = h
        elif t > 0:
            # Time known, find height and velocity
            h = 0.5 * g * t * t
            v = g * t
            results['height'] = h
            results['final_velocity'] = v
            results['time'] = t
        elif v0 > 0 and t > 0:
            # Initial velocity and time
            h = v0 * t + 0.5 * g * t * t
            v = v0 + g * t
            results['height'] = h
            results['final_velocity'] = v
            results['time'] = t
        
        return results
