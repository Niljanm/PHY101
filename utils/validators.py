"""
Input Validation Utilities
Helper functions for validating and parsing user inputs
"""

def safe_float(value, field_name="Value"):
    """
    Safely parse a string to float with error handling
    
    Args:
        value: String value to parse
        field_name: Name of the field for error messages
        
    Returns:
        float: Parsed floating point number
        
    Raises:
        ValueError: If value is empty or cannot be parsed
    """
    if not value or value.strip() == "":
        raise ValueError(f"{field_name} cannot be empty!")
    
    try:
        result = float(value.strip())
        return result
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number!")


def validate_positive(value, field_name="Value"):
    """
    Validate that a value is positive
    
    Args:
        value: Numeric value to check
        field_name: Name of the field for error messages
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{field_name} must be positive!")
    return True


def validate_non_negative(value, field_name="Value"):
    """
    Validate that a value is non-negative
    
    Args:
        value: Numeric value to check
        field_name: Name of the field for error messages
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If value is negative
    """
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative!")
    return True


def validate_non_zero(value, field_name="Value"):
    """
    Validate that a value is not zero
    
    Args:
        value: Numeric value to check
        field_name: Name of the field for error messages
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If value is zero
    """
    if value == 0:
        raise ValueError(f"{field_name} cannot be zero!")
    return True


def validate_range(value, min_val, max_val, field_name="Value"):
    """
    Validate that a value is within a specified range
    
    Args:
        value: Numeric value to check
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field for error messages
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If value is outside the range
    """
    if value < min_val or value > max_val:
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}!")
    return True


def parse_multiple_floats(values_dict, required_fields=None):
    """
    Parse multiple string values to floats
    
    Args:
        values_dict: Dictionary of field_name: string_value pairs
        required_fields: List of field names that must be filled
        
    Returns:
        dict: Dictionary of field_name: float_value pairs
        
    Raises:
        ValueError: If any required field is missing or invalid
    """
    result = {}
    
    if required_fields:
        for field in required_fields:
            if field not in values_dict or not values_dict[field]:
                raise ValueError(f"{field} is required!")
    
    for field_name, string_value in values_dict.items():
        if string_value and string_value.strip():
            result[field_name] = safe_float(string_value, field_name)
        else:
            result[field_name] = None
    
    return result
