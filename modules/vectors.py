"""Vectors Module"""
import math

class Vectors:
    @staticmethod
    def calculate_vector_magnitude(x=0, y=0, z=0):
        """Calculate magnitude of a vector"""
        magnitude = math.sqrt(x*x + y*y + z*z)
        return {'magnitude': magnitude}
    
    @staticmethod
    def calculate_vector_addition(x1=0, y1=0, x2=0, y2=0):
        """Add two 2D vectors"""
        result_x = x1 + x2
        result_y = y1 + y2
        magnitude = math.sqrt(result_x*result_x + result_y*result_y)
        
        return {
            'resultant_x': result_x,
            'resultant_y': result_y,
            'magnitude': magnitude
        }
    
    @staticmethod
    def calculate_dot_product(x1=0, y1=0, x2=0, y2=0):
        """Calculate dot product of two vectors"""
        dot = x1*x2 + y1*y2
        return {'dot_product': dot}
    
    @staticmethod
    def calculate_angle_between(x1=0, y1=0, x2=0, y2=0):
        """Calculate angle between two vectors"""
        mag1 = math.sqrt(x1*x1 + y1*y1)
        mag2 = math.sqrt(x2*x2 + y2*y2)
        
        if mag1 == 0 or mag2 == 0:
            return {'angle': 0}
        
        dot = x1*x2 + y1*y2
        cos_angle = dot / (mag1 * mag2)
        angle_rad = math.acos(max(-1, min(1, cos_angle)))
        angle_deg = math.degrees(angle_rad)
        
        return {'angle_degrees': angle_deg, 'angle_radians': angle_rad}
