import json
import os
import unit_converter_new
from rounding import round_number


def compute_homa_ir(input_variables):

    if input_variables["insulin"][1] == "pmol/L":
        input_variables["insulin"][0] =  input_variables["insulin"][0] * 6
    elif input_variables["insulin"][1] == "ng/mL":
        input_variables["insulin"][0] = input_variables["insulin"][0] * 24.8

    #insulin = unit_converter_new.conversions(input_variables["insulin"][0], input_variables["insulin"][1], "µIU/mL", 5734, None )
    glucose = unit_converter_new.conversions(input_variables["glucose"][0], input_variables["glucose"][1], "mg/dL", 180.16, None)

    return (input_variables["insulin"][0] * glucose)/405


def compute_homa_ir_explanation(input_variables):

    explanation = "The formula for computing HOMA-IR score is (insulin (µIU/mL) * glucose mg/dL)/405.\n"

    insulin = input_variables["insulin"][0]

    if input_variables["insulin"][1] == "µIU/mL":
        explanation += f"The concentration of insulin is {insulin} µIU/mL.\n"
    
    elif input_variables["insulin"][1] == "pmol/L":
        insulin =  input_variables["insulin"][0] * 6
        explanation += f"The concentration of insulin is {insulin} pmol/L. We to need convert the concentration of insulin to pmol/L, by multiplying by the conversion factor of 6.0 µIU/mL/pmol/L. This makes the insulin concentration {input_variables['insulin'][0]} * 6 µIU/mL/pmol/L = {insulin} µIU/mL.\n"

    elif input_variables["insulin"][1] == "ng/mL":
        insulin = input_variables["insulin"][0] * 24.8
        explanation += f"The concentration of insulin is {insulin} ng/mL. We to need convert the concentration of insulin to µIU/mL, by multiplying by the conversion factor 24.8 µIU/mL/ng/mL. This makes the insulin concentration {input_variables['insulin'][0]} * 24.8 µIU/mL/ng/mL = {insulin} ng/mL.\n"

    #insulin_exp, insulin = unit_converter_new.conversion_explanation(input_variables["insulin"][0], "insulin", 5734, None, input_variables["glucose"][1], "µIU/mL")
    glucose_exp, glucose = unit_converter_new.conversion_explanation(input_variables["glucose"][0], "glucose", 180.16, None, input_variables["glucose"][1], "mg/dL")

    explanation += glucose_exp + "\n"

    answer = round_number((insulin * glucose)/405)

    explanation += f"Plugging into the formula will give us {insulin} * {glucose}/405 = {answer}. Hence, the patient's HOMA-IR score is {answer}. \n"

    return {"Explanation": explanation, "Answer": answer, "Calculator Answer": compute_homa_ir(input_variables)}


output = {}

test_outputs = [
    {
        'insulin': [12.43, "µIU/mL"],
        'glucose': [85.23, "mg/dL"]
    },
    {
        'insulin': [74.58, "pmol/L"],
        'glucose': [4.73, "mmol/dL"]
    }
]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_homa_ir_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/homa_ir.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/homa_ir.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

