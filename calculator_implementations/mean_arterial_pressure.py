from rounding import round_number

def mean_arterial_pressure_explanation(variables):

    sys_bp = variables['sys_bp']
    dia_bp = variables['dia_bp']
    
    output = ""

    value = round_number(sys_bp[0]/3 + 2*dia_bp[0]/3)

    output += f"The mean average pressure is computed by the formula 1/3 * (systolic blood pressure) + 2/3 * (diastolic blood pressure). Plugging in the values, we get 1/3 * {sys_bp[0]} mm Hg + 2/3 * {dia_bp[0]} mm Hg = {value} mm Hg.\n"
    output += f"Hence, the patient's mean arterial pressure is {value} mm Hg."

    return {"Explanation": output, "Answer": value}
