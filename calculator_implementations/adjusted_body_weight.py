import json
import weight_conversion
import ideal_body_weight
import os
from rounding import round_number

def abw_calculator(input_variables):

    gender = input_variables["sex"]

    weight = weight_conversion.weight_conversion(input_variables["weight"])

    ibw = ideal_body_weight.ibw_calculator({"sex": gender, "height": input_variables["height"]})

    abw = ibw + 0.4 * (weight - ibw)

    return abw


def abw_explanation(input_variables):

    weight_explanation, weight = weight_conversion.weight_conversion_explanation(input_variables["weight"])
    ibw_explanation =  ideal_body_weight.ibw_explanation(input_variables)

    explanation = f"{ibw_explanation['Explanation']}"
    explanation += f"{weight_explanation}"
   

    ibw = ibw_explanation["Answer"]
        
    abw = round_number(ibw + 0.4 * (weight - ibw))
    abw_explanation_string = ""
    abw_explanation_string += f"To compute the ABW value, apply the following formula: "
    abw_explanation_string += f"ABW = IBW + 0.4 * (weight (in kg) - IBW (in kg)). "
    abw_explanation_string += f"ABW = {ibw} kg + 0.4 * ({weight} kg  - {ibw} kg) = {abw} kg. "
    abw_explanation_string += f"The patient's adjusted body weight is {abw} kg.\n"

    explanation += abw_explanation_string

    return {"Explanation": explanation, "ABW": abw_explanation_string, "Answer": abw, "Calculator Answer": abw_calculator(input_variables)}


outputs = {}

test_outputs = [ {"weight": [123, "lbs"],  "height": [5, "ft", 2.5, "in"], "sex": "Male"}, {"weight": [40.3 , "kg"], "height": [120.3, "cm"], "sex": "Female"},
{"weight": [54.1, "kg"] , "height": [73.2, "in"], "sex": "Female"}]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = abw_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/adjusted_body_weight.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/adjusted_body_weight.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)