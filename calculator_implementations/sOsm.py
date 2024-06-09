import os
import json
import unit_converter_new
from rounding import round_number


def compute_serum_osmolality(input_parameters):
    
    sodium = unit_converter_new.conversions(input_parameters["sodium"][0], input_parameters["sodium"][1], "mmol/L", 22.99, 1)
    bun = unit_converter_new.conversions(input_parameters["bun"][0], input_parameters["bun"][1], "mg/dL", 28.02, None)
    glucose = unit_converter_new.conversions(input_parameters["glucose"][0], input_parameters["glucose"][1], "mg/dL", 180.16, None)

    return 2 * sodium + (bun / 2.8) + (glucose / 18)



def compute_serum_osmolality_explanation(input_parameters):

    explanation = "The formula for computing serum osmolality is 2 * Na + (BUN / 2.8) + (glucose / 18), where Na is the concentration of sodium in mmol/L, the concentration of BUN is in mg/dL, and the concentration of glucose is in mg/dL.\n"
    
    sodium_exp, sodium = unit_converter_new.conversion_explanation(input_parameters["sodium"][0], "sodium", 22.99, 1, input_parameters["sodium"][1], "mmol/L")
    bun_exp, bun = unit_converter_new.conversion_explanation(input_parameters["bun"][0], "bun", 28.02, None, input_parameters["bun"][1], "mg/dL")
    glucose_exp, glucose = unit_converter_new.conversion_explanation(input_parameters["glucose"][0], "glucose", 180.16, None, input_parameters["glucose"][1], "mg/dL")

    explanation += sodium_exp + "\n"
    explanation += bun_exp + "\n"
    explanation += glucose_exp + "\n"

    serum_os = round_number(2 * sodium + (bun / 2.8) + (glucose / 18))

    explanation += f"Plugging these values into the equation, we get 2 * {sodium} + ({bun} / 2.8) + ({bun} / 18) = {serum_os} mmol/L."
    explanation += f"The patient's calculated serum osmolality concentration is {serum_os} mmol/L. This is equalivalent to {serum_os} mOsm/kg.\n"

    return {"Explanation": explanation, "Answer": serum_os, "Calculator Answer": compute_serum_osmolality(input_parameters)}


test_outputs = [{"sodium": [140, "mEq/L"], "bun": [14.01, "mg/dL"], "glucose": [80, "mg/dL"]}, 
              {"sodium": [140.0, "mmol/L"], "bun": [5.00, "mmol/L"], "glucose": [4.44, "mmol/L"]}
              ]

outputs = ""
for i, test_case in enumerate(test_outputs):
    outputs += "Explanation:" + "\n"+  compute_serum_osmolality_explanation(test_case)["Explanation"] + "\n"


file_name = "explanations/sOsm.txt"

with open(file_name, 'w') as file:
    file.write(outputs)