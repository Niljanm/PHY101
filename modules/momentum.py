"""Momentum Module"""

class Momentum:
    @staticmethod
    def calculate(m1=0, v1=0, m2=0, v2=0):
        """Calculate momentum"""
        results = {}
        
        if m1 > 0 and v1 != 0:
            p1 = m1 * v1
            results['p1'] = p1
        
        if m2 > 0 and v2 != 0:
            p2 = m2 * v2
            results['p2'] = p2
        
        if m1 > 0 and v1 != 0 and m2 > 0 and v2 != 0:
            p1 = m1 * v1
            p2 = m2 * v2
            p_total = p1 + p2
            results['p1'] = p1
            results['p2'] = p2
            results['p_total'] = p_total
        
        return results
