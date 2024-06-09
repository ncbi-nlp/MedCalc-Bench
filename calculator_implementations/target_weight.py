import json
import height_conversion
from rounding import round_number

def target_weight(input_variables):

    bmi = input_variables["body_mass_index"][0]
    height = height_conversion.height_conversion(input_variables["height"])

    target_weight = bmi * (height * height)

    return target_weight

def targetweight_explanation(input_variables):

    bmi  = input_variables["body_mass_index"][0]
    height_exp, height = height_conversion.height_conversion_explanation(input_variables["height"])
    target_weight_val = round_number(bmi * (height * height))

    explanation = ""

    explanation += f"The patient's target bmi is {bmi} kg/m^2. "

    explanation += f"{height_exp}"
    
    explanation += f"From this, the patient's target weight is {bmi} kg/m^2 * {height} m * {height} m = {target_weight_val} kg. "
   
    return {"Explanation": explanation, "Answer": target_weight_val, "Calculator Answer": target_weight(input_variables)}


test_cases = [{"body_mass_index": [22], "height": [5, "ft", 7, "in"]}, {"body_mass_index": [19.4, "kg/m^2"], "height": [120, "cm"]}, {"body_mass_index": [23.1, "kg/m^2"], "height": [74.5, "in"]},  {"body_mass_index": [22.5, "kg/m^2"], "height": [5, "ft"]}]

outputs = {}

text = ""

for i in range(len(test_cases)):

    text += "Explanation:\n" + targetweight_explanation(test_cases[i])["Explanation"] + "\n"

file_name = "explanations/target_weight.txt"

with open(file_name, 'w') as file:
    file.write(text)

'''
file_name = "explanations/target_weight_explanations.json"

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

