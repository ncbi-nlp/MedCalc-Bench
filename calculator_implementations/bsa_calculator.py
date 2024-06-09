import math
import height_conversion
import weight_conversion
import json
import os
from rounding import round_number

def bsa_calculator(input_variables):

    weight = weight_conversion.weight_conversion(input_variables["weight"])
    height = height_conversion.height_conversion_cm(input_variables["height"])

    result = math.sqrt((weight * height)/3600)

    return result 

def bsa_calculator_explaination(input_variables):

    height_explaination, height = height_conversion.height_conversion_explanation_cm(input_variables["height"])
    weight_explanation, weight = weight_conversion.weight_conversion_explanation(input_variables["weight"])
    
    output = "For the body surface area computation, the formula is sqrt((weight (in kgs) * height (in cm))/3600, where the units of weight is in kg and the units of height is in cm.\n"

    output += height_explaination + "\n"
    output += weight_explanation + "\n"
 
    answer = round_number(math.sqrt(weight * height/3600))
    output += f"Therefore, the patient's bsa is sqrt(({weight} (in kgs) * {height} (in cm))/3600) = {answer} m^2."

    return {"Explanation": output, "Answer": answer, "Calculator Answer" : bsa_calculator(input_variables)}



test_samples = [{"weight": [150.1, "lbs"], "height": [5, "ft", 2.5, "in"]}, 
                {"weight": [32.1, "kg"], "height": [120.3, "cm"]}, 
                {"weight": [100, "kg"], "height": [73.2, "in"]},
                {"weight": [131, "kg"], "height": [7, "ft"]} ]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_samples):
    outputs[i] = bsa_calculator_explaination(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/bsa.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/bsa.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)





