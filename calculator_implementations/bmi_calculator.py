import json
import os 
import height_conversion
import weight_conversion
from rounding import round_number


def bmi_calculator(input_variables):

    weight = input_variables["weight"][0]
    w_label = input_variables["weight"][1]

    if len(input_variables["height"]) == 4:
        input_variables["height"] = [input_variables["height"][0] * 12 + input_variables["height"][2], "in"]

    height = input_variables["height"][0]
    h_label = input_variables["height"][1]

    if w_label == "lbs":
        weight = weight_conversion.weight_conversion(input_variables["weight"])

    if h_label == "in" or h_label == "cm":
        height = height_conversion.height_conversion(input_variables["height"])

    return weight/(height * height)

def bmi_calculator_explanation(input_variables):

    height_explanation, height = height_conversion.height_conversion_explanation(input_variables["height"])
    weight_explanation, weight = weight_conversion.weight_conversion_explanation(input_variables["weight"])

    output = "The formula for computing the patient's BMI is (weight)/(height * height), where weight is the patient's weight in kg and height is the patient's height in m.\n"

    output += height_explanation
    output += weight_explanation
    result = round_number(weight/(height * height))
    output += f"The patient's bmi is therefore {weight} kg / ({height} m * {height} m) = {result} kg/m^2."

    return {"Explanation": output, "Answer": result, "Calculator Answer": bmi_calculator(input_variables)}
    

test_outputs = [{"weight": [150.1, "lbs"], "height": [5, "ft", 2.5, "in"]}, {"weight": [32.1, "kg"], "height": [120.3, "cm"]},
{"weight": [100, "kg"], "height": [73.2, "in"]}, {"weight": [174.10, "lbs"], "height": [67, "in"]}]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = bmi_calculator_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/gbs.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/bmi_calculator.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

