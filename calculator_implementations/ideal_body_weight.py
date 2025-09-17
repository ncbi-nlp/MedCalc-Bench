import height_conversion
from rounding import round_number

def ibw_explanation(input_variables):

    height = input_variables["height"]
    gender = input_variables["sex"]

    explanation = (f"For males, the ideal body weight (IBW) is calculated as follows: IBW = 50 kg + 2.3 kg * (height (in inches) - 60)\n")
    explanation += (f"For females, the ideal body weight (IBW) is calculated as follows: 45.5 kg + 2.3 kg * (height (in inches) - 60)\n")

    height_explanation, height = height_conversion.height_conversion_explanation_in(input_variables["height"])

    explanation += f"The patient's gender is {gender}.\n"
    explanation += f"{height_explanation}\n"

    if gender == "Male":
        ibw = round_number(50 + 2.3 * (height - 60))
        explanation += (f"Plugging in the values for the IBW formula for males gives us 50 kg + 2.3 kg * ({height} (in inches) - 60) = {ibw} kg.\n")
                   
    elif gender == "Female":
        ibw = round_number(45.5 + 2.3 * (height - 60))
        explanation += (f"Plugging in the values for the IBW formula for females gives us 45.5 kg + 2.3 kg * ({height} (in inches) - 60) = {ibw} kg.\n")
        
    explanation += f"Hence, the patient's IBW is {ibw} kg."
    
    return {"Explanation": explanation, "Answer": ibw}



