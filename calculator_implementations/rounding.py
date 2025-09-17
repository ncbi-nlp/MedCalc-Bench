from math import log10, floor

def round_number(num):
    """
    Rounds numbers based on their magnitude to preserve appropriate precision:
    1. For numbers >= 0.0001 (absolute value): rounds to 5 decimal places
    2. For numbers < 0.0001 (absolute value): preserves 5 significant digits
    
    This ensures small numbers like 0.000085 or 0.000015 keep their precision.
    Works correctly with both positive and negative numbers.
    """
    if num == 0:
        return 0
        
    # Get number of significant digits in decimal representation
    # Using absolute value to handle negative numbers correctly
    sig_digits = -int(floor(log10(abs(num)))) + 5
    
    # For larger numbers (>= 0.0001 in absolute value), cap at 5 decimal places
    if abs(num) >= 1e-4:
        return round(num, 5)
    else:
        # For smaller numbers, preserve appropriate significant digits
        return round(num, sig_digits)
