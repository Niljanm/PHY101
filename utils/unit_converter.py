"""
Unit Conversion Utilities
Convert between different unit systems
"""

class UnitConverter:
    """Static class for unit conversions"""
    
    # Speed conversions
    SPEED_CONVERSIONS = {
        "m/s": 1.0,
        "km/h": 3.6,
        "mph": 2.237,
        "ft/s": 3.281,
        "knots": 1.944
    }
    
    # Mass conversions
    MASS_CONVERSIONS = {
        "kg": 1.0,
        "g": 1000.0,
        "mg": 1000000.0,
        "lb": 2.205,
        "oz": 35.274
    }
    
    # Distance conversions
    DISTANCE_CONVERSIONS = {
        "m": 1.0,
        "cm": 100.0,
        "mm": 1000.0,
        "km": 0.001,
        "ft": 3.281,
        "in": 39.37,
        "mile": 0.000621
    }
    
    # Energy conversions
    ENERGY_CONVERSIONS = {
        "J": 1.0,
        "kJ": 0.001,
        "MJ": 0.000001,
        "cal": 0.239,
        "kcal": 0.000239,
        "eV": 6.242e18,
        "Wh": 0.000278
    }
    
    # Voltage conversions (mainly scaling)
    VOLTAGE_CONVERSIONS = {
        "V": 1.0,
        "kV": 0.001,
        "mV": 1000.0,
        "μV": 1000000.0
    }
    
    @staticmethod
    def convert_speed(value, from_unit, to_unit):
        """Convert speed between units"""
        if from_unit not in UnitConverter.SPEED_CONVERSIONS:
            raise ValueError(f"Unknown speed unit: {from_unit}")
        if to_unit not in UnitConverter.SPEED_CONVERSIONS:
            raise ValueError(f"Unknown speed unit: {to_unit}")
        
        base_value = value / UnitConverter.SPEED_CONVERSIONS[from_unit]
        return base_value * UnitConverter.SPEED_CONVERSIONS[to_unit]
    
    @staticmethod
    def convert_mass(value, from_unit, to_unit):
        """Convert mass between units"""
        if from_unit not in UnitConverter.MASS_CONVERSIONS:
            raise ValueError(f"Unknown mass unit: {from_unit}")
        if to_unit not in UnitConverter.MASS_CONVERSIONS:
            raise ValueError(f"Unknown mass unit: {to_unit}")
        
        base_value = value / UnitConverter.MASS_CONVERSIONS[from_unit]
        return base_value * UnitConverter.MASS_CONVERSIONS[to_unit]
    
    @staticmethod
    def convert_distance(value, from_unit, to_unit):
        """Convert distance between units"""
        if from_unit not in UnitConverter.DISTANCE_CONVERSIONS:
            raise ValueError(f"Unknown distance unit: {from_unit}")
        if to_unit not in UnitConverter.DISTANCE_CONVERSIONS:
            raise ValueError(f"Unknown distance unit: {to_unit}")
        
        base_value = value / UnitConverter.DISTANCE_CONVERSIONS[from_unit]
        return base_value * UnitConverter.DISTANCE_CONVERSIONS[to_unit]
    
    @staticmethod
    def convert_energy(value, from_unit, to_unit):
        """Convert energy between units"""
        if from_unit not in UnitConverter.ENERGY_CONVERSIONS:
            raise ValueError(f"Unknown energy unit: {from_unit}")
        if to_unit not in UnitConverter.ENERGY_CONVERSIONS:
            raise ValueError(f"Unknown energy unit: {to_unit}")
        
        base_value = value / UnitConverter.ENERGY_CONVERSIONS[from_unit]
        return base_value * UnitConverter.ENERGY_CONVERSIONS[to_unit]
    
    @staticmethod
    def convert_voltage(value, from_unit, to_unit):
        """Convert voltage between units"""
        if from_unit not in UnitConverter.VOLTAGE_CONVERSIONS:
            raise ValueError(f"Unknown voltage unit: {from_unit}")
        if to_unit not in UnitConverter.VOLTAGE_CONVERSIONS:
            raise ValueError(f"Unknown voltage unit: {to_unit}")
        
        base_value = value / UnitConverter.VOLTAGE_CONVERSIONS[from_unit]
        return base_value * UnitConverter.VOLTAGE_CONVERSIONS[to_unit]
