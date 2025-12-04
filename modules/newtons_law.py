"""Newton's Law of Motion Module"""

class NewtonsLaw:
    @staticmethod
    def calculate(f=0, m=0, a=0):
        """Calculate using Newton's Second Law: F = ma
        
        Args:
            f: Force (N)
            m: Mass (kg)
            a: Acceleration (m/s²)
        
        Returns:
            Dictionary with calculated values
        """
        results = {}
        
        # F = ma
        if f == 0 and m > 0 and a > 0:
            results['force'] = m * a
        elif m == 0 and f > 0 and a > 0:
            results['mass'] = f / a
        elif a == 0 and f > 0 and m > 0:
            results['acceleration'] = f / m
        else:
            # If multiple values provided, calculate all possible results
            if m > 0 and a > 0:
                results['force'] = m * a
            if f > 0 and a > 0:
                results['mass'] = f / a
            if f > 0 and m > 0:
                results['acceleration'] = f / m
        
        return results
