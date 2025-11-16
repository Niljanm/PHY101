"""Work and Energy Module"""

class WorkEnergy:
    @staticmethod
    def calculate_work_energy(force=0, distance=0, mass=0, velocity=0, height=0, g=9.8):
        """Calculate work and energy"""
        results = {}
        
        if force > 0 and distance > 0:
            work = force * distance
            results['work'] = work
        
        if mass > 0 and velocity > 0:
            ke = 0.5 * mass * velocity * velocity
            results['kinetic_energy'] = ke
        
        if mass > 0 and height > 0:
            pe = mass * g * height
            results['potential_energy'] = pe
        
        if mass > 0 and velocity > 0 and height > 0:
            ke = 0.5 * mass * velocity * velocity
            pe = mass * g * height
            total_e = ke + pe
            results['kinetic_energy'] = ke
            results['potential_energy'] = pe
            results['total_energy'] = total_e
        
        return results
