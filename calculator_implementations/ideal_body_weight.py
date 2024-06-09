import json
import height_conversion
import os
from rounding import round_number

def ibw_calculator(input_variables):
    
    height = height_conversion.height_conversion_in(input_variables["height"])
    gender = input_variables["sex"]
    
    if gender == "Male":
        ibw = 50 + 2.3 * (height - 60)
    elif gender == "Female":
        ibw = 45.5 + 2.3 * (height - 60)

    return ibw

def ibw_explanation(input_variables):

    height = input_variables["height"]
    gender = input_variables["sex"]

    explanation = ""

    height_explanation, height = height_conversion.height_conversion_explanation_in(input_variables["height"])

    explanation += f"The patient's gender is {gender}.\n"
    explanation += f"{height_explanation}\n"

    if gender == "Male":
        ibw = round_number(50 + 2.3 * (height - 60))
        explanation += (f"For males, the ideal body weight (IBW) is calculated as follows:\n"
                       f"IBW = 50 kg + 2.3 kg * (height (in inches) - 60)\n"
                       f"Plugging in the values gives us 50 kg + 2.3 kg * ({height} (in inches) - 60) = {ibw} kg.\n")
                   
    elif gender == "Female":
        ibw = round_number(45.5 + 2.3 * (height - 60))
        explanation += (f"For females, the ideal body weight (IBW) is calculated as follows:\n"
                       f"IBW = 45.5 kg + 2.3 kg * (height (in inches) - 60)\n"
                       f"Plugging in the values gives us 45.5 kg + 2.3 kg * ({height} (in inches) - 60) = {ibw} kg.\n")
        
    explanation += f"Hence, the patient's IBW is {ibw} kg."
    
    return {"Explanation": explanation, "Answer": ibw, "Calculator Answer": ibw_calculator(input_variables)}


outputs = {}

test_outputs = [{"height": [5, "ft", 2.5, "in"], "sex": "Male"}, {"height": [120, "cm"], "sex": "Male"},
{"height": [120.3, "cm"], "sex": "Female"},
{"height": [73.2, "in"], "sex": "Female"}]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = ibw_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/ideal_body_weight.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/ideal_body_weight.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)


