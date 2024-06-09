import os
import json 
import weight_conversion
from rounding import round_number


def maintenance_fluid(input_parameters):

    weight = weight_conversion.weight_conversion(input_parameters["weight"])

    if weight <= 10:
        return weight * 4
    elif 10 < weight <= 20:
        return 40 + 2 * (weight - 10)
    elif weight > 20:
        return 60 + (weight - 20)


def maintenance_fluid_explanation(input_parameters):

    weight_exp, weight = weight_conversion.weight_conversion_explanation(input_parameters["weight"])

    explanation = ""

    explanation += weight_exp

    if weight < 10:
        answer = round_number(weight * 4)
        explanation += f"For patient's with weight less than 10 kg, the rule for computing maintenance fluid is to multiply their weight by 4 mL/kg/hr to get the maintenance fluids per hour. Hence, the patient's maintenance fluid is {weight} kg * 4 mL/kg/hr = {answer} mL/hr.\n"
    elif 10 <= weight <= 20:
        answer = round_number(40 + 2 * (weight - 10))
        explanation += f"For patient's whose weight is in between 10 kg and 20 kg, the formula for computing maintenance fluid is 40 mL/hr + 2 mL/kg/hr * (weight (in kilograms) - 10 kilograms). Hence, plugging into this formula, we get 40 mL/hr + 2 mL/kg/hr * ({weight} kg - 10 kg) = {answer} mL/hr.\n"
    elif weight > 20:
        answer = round_number(60 + (weight - 20))
        explanation += f"For patient's whose weight is greater than 20 kg, the formula for computing the maintenance fluid is 60 mL/hr + 1 mL/kg/hr * (weight (in kilograms) - 20 kilograms). Hence, plugging into this formula, we get 60 mL/hr + 2 mL/kg/hr * ({weight} kg - 20 kg) = {answer} mL/hr.\n"

    explanation += f"Hence, the patient's fluid maintenance is {answer} mL/hr.\n"

    return {"Explanation": explanation, "Answer": answer, "Calculator Answer": maintenance_fluid(input_parameters)}


test_outputs = [
    {"weight": [220.26, "lbs"]},  
    {"weight": [100, "kg"]},  
    {"weight": [11, "kg"]}, 
    {"weight": [24.25, "lbs"]},  
    {"weight": [5, "kg"]}, 
    {"weight": [11.07, "lbs"]}, 

]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] =  maintenance_fluid_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/maintenance_fluid.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/maintenance_fluid.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

