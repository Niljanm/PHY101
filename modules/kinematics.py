"""Kinematics Module"""
import math

class Kinematics:
    @staticmethod
    def calculate(u=0, a=0, t=0, s=0, v=0):
        """Calculate kinematics using equations of motion"""
        results = {}
        
        # v = u + at
        if t != 0 and a != 0:
            if v == 0:
                v = u + a * t
                results['v'] = v
        
        # s = ut + 0.5*a*t^2
        if t != 0 and a != 0:
            if s == 0:
                s = u * t + 0.5 * a * t * t
                results['s'] = s
        
        # v^2 = u^2 + 2as
        if a != 0 and s != 0:
            v_squared = u * u + 2 * a * s
            if v_squared >= 0 and v == 0:
                v = math.sqrt(v_squared)
                results['v'] = v
        
        # Solve for missing values
        if t != 0 and v != 0 and u != 0 and a == 0:
            a = (v - u) / t
            results['a'] = a
        
        if a != 0 and v != 0 and u != 0 and t == 0:
            t = (v - u) / a
            results['t'] = t
        
        if s != 0 and u != 0 and t != 0 and a == 0:
            a = (2 * (s - u * t)) / (t * t)
            results['a'] = a
        
        return results
