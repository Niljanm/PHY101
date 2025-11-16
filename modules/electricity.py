"""Electricity Module"""

class Electricity:
    @staticmethod
    def calculate_ohms_law(v=0, i=0, r=0):
        """Calculate Ohm's Law: V = IR"""
        results = {}
        
        if v > 0 and i > 0:
            r = v / i
            results['resistance'] = r
        elif v > 0 and r > 0:
            i = v / r
            results['current'] = i
        elif i > 0 and r > 0:
            v = i * r
            results['voltage'] = v
        
        if v > 0 and i > 0:
            power = v * i
            results['power'] = power
        
        return results
    
    @staticmethod
    def calculate_coulombs_law(q1=0, q2=0, r=1, k=8.99e9):
        """Calculate Coulomb's Law"""
        if q1 > 0 and q2 > 0 and r > 0:
            force = k * (q1 * q2) / (r * r)
            return {'force': force, 'distance': r}
        return {}
