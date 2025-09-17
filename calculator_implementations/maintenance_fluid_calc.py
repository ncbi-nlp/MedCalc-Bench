import weight_conversion
from rounding import round_number


def maintenance_fluid_explanation(input_parameters):

    weight_exp, weight = weight_conversion.weight_conversion_explanation(input_parameters["weight"])

    explanation = "For patient's with weight less than 10 kg, the rule for computing maintenance fluid is to multiply their weight by 4 mL/kg/hr to get the maintenance fluids per hour.\n"
    explanation += "For patient's with weight between 10 kg and 20 kg, the formula for computing maintenance fluid is 40 mL/hr + 2 mL/kg/hr * (weight (in kilograms) - 10 kilograms).\n"
    explanation += "For patient's with weight greater than 20 kg, the formula for computing the maintenance fluid is 60 mL/hr + 1 mL/kg/hr * (weight (in kilograms) - 20 kilograms).\n"

    explanation += weight_exp

    if weight < 10:
        answer = round_number(weight * 4)
        explanation += f"Hence, the patient's maintenance fluid is {weight} kg * 4 mL/kg/hr = {answer} mL/hr.\n"
    elif 10 <= weight <= 20:
        answer = round_number(40 + 2 * (weight - 10))
        explanation += f"Hence, plugging into this formula, we get 40 mL/hr + 2 mL/kg/hr * ({weight} kg - 10 kg) = {answer} mL/hr.\n"
    elif weight > 20:
        answer = round_number(60 + (weight - 20))
        explanation += f"Hence, plugging into this formula, we get 60 mL/hr + 1 mL/kg/hr * ({weight} kg - 20 kg) = {answer} mL/hr.\n"

    explanation += f"Hence, the patient's fluid maintenance is {answer} mL/hr."

    return {"Explanation": explanation, "Answer": answer}



