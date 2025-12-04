"""Potential Energy and Kinetic Energy Module"""

class PEandKE:
    @staticmethod
    def calculate(m=0, h=0, v=0, g=9.8):
        """Calculate potential and kinetic energy
        
        Args:
            m: Mass (kg)
            h: Height (m)
            v: Velocity (m/s)
            g: Gravitational acceleration (m/s²)
        
        Returns:
            Dictionary with energy values
        """
        results = {}
        
        # Potential Energy: PE = mgh
        if m > 0 and h > 0:
            pe = m * g * h
            results['potential_energy'] = pe
        
        # Kinetic Energy: KE = 0.5 * m * v²
        if m > 0 and v > 0:
            ke = 0.5 * m * v * v
            results['kinetic_energy'] = ke
        
        # Total Energy
        pe = m * g * h if (m > 0 and h > 0) else 0
        ke = 0.5 * m * v * v if (m > 0 and v > 0) else 0
        
        if pe > 0 or ke > 0:
            results['total_energy'] = pe + ke
        
        return results
