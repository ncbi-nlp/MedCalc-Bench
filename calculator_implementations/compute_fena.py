import os
import json
import unit_converter_new
from rounding import round_number


def compute_fena(input_variables):

    sodium = unit_converter_new.conversions(input_variables["sodium"][0], input_variables["sodium"][1], "mEq/L", 22.99, 1)
    creatinine = unit_converter_new.conversions(input_variables["creatinine"][0], input_variables["creatinine"][1], "mg/dL", 113.12 , None)
    urine_sodium = unit_converter_new.conversions(input_variables["urine_sodium"][0], input_variables["urine_sodium"][1], "mEq/L", None , 1)
    urine_creatinine = unit_converter_new.conversions(input_variables["urine_creatinine"][0], input_variables["urine_creatinine"][1], "mg/dL", 113.12, None)
    
    return (creatinine * urine_sodium)/(sodium * urine_creatinine) * 100

def compute_fena_explanation(input_variables):

    explanation = "The formula for computing the FEna percentage is (creatinine * urine_sodium)/(sodium * urine_creatinine) * 100, where creatinine is the concentration in mg/dL, urine sodium is the concentration in mEq/L, sodium is the concentration mEq/L, and urine creatinine is the concentration in mg/dL.\n"

    sodium_exp, sodium = unit_converter_new.conversion_explanation(input_variables["sodium"][0], "sodium", 22.99, 1, input_variables["sodium"][1], "mEq/L")
    creatinine_exp, creatinine = unit_converter_new.conversion_explanation(input_variables["creatinine"][0], "creatinine", 113.12, 1, input_variables["creatinine"][1], "mg/dL")
    urine_sodium_exp, urine_sodium  = unit_converter_new.conversion_explanation(input_variables["urine_sodium"][0], "urine sodium", 22.99, 1, input_variables["urine_sodium"][1], "mEq/L")
    urine_creatinine_exp, urine_creatinine = unit_converter_new.conversion_explanation(input_variables["urine_creatinine"][0], "urine creatinine", 113.12, 1, input_variables["urine_creatinine"][1], "mg/dL")
    
    explanation += sodium_exp  + '\n'
    explanation += creatinine_exp  + '\n'
    explanation += urine_creatinine_exp  + '\n'
    explanation += urine_sodium_exp  + '\n'

    result = round_number((creatinine * urine_sodium)/(sodium * urine_creatinine) * 100)

    explanation += f"Plugging in these values, we get 100 * ({creatinine} * {urine_sodium})/({sodium} * {urine_creatinine}) = {result} % FENa.\n"
    explanation += f"Hence, the patient's FEna percentage is {result} %.\n"

    return {"Explanation": explanation, "Answer": result, "Calculator Answer": compute_fena(input_variables)}


test_outputs = [{"sodium": [140.0, "mEq/L"], "creatinine": [99.89, "µmol/L"], "urine_sodium": [130, "mmol/L"], "urine_creatinine": [2000, "µmol/L"]}, 
                {"sodium": [140.0, "mmol/L"], "creatinine": [1.13, "mg/dL"], "urine_sodium": [130, "mEq/L"], "urine_creatinine": [22.62, "mg/dL"]}, 
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_fena_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/fena.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/fena.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

 
    
