import os
import json
import unit_converter_new
from rounding import round_number


def compute_sodium_correction_hyperglycemia(input_variables):

    sodium = input_variables["sodium"]
    glucose = input_variables["glucose"]

    sodium = unit_converter_new.conversions(sodium[0], sodium[1], "mEq/L", 22.99, 1)
    glucose = unit_converter_new.conversions(glucose[0], glucose[1], "mg/dL", 180.16, None)

    return sodium + 0.024 * (glucose - 100)


def compute_sodium_correction_hyperglycemia_explanation(input_variables):

    sodium = input_variables["sodium"]
    glucose = input_variables["glucose"]

    sodium_explanation, sodium = unit_converter_new.conversion_explanation(sodium[0], "sodium", 22.99, 1, sodium[1], "mEq/L")
    glucose_explanation, glucose = unit_converter_new.conversion_explanation(glucose[0], "glucose", 180.16, None, glucose[1], "mg/dL")

    corrected_sodium = round_number(sodium + 0.024 * (glucose - 100))

    explanation = "The formula for Sodium Correction for Hyperglycemia is Measured sodium + 0.024 * (Serum glucose - 100), where Measured Sodium is the sodium concentration in mEq/L and the Serum glucose is the concentration of glucose in mg/dL.\n"

    explanation += sodium_explanation + "\n"
    explanation += glucose_explanation + "\n"

    explanation += f"Plugging in these values into the formula gives us {sodium} mEq/L + 0.024 * ({glucose} - 100) = {corrected_sodium} mEq/L.\n"

    explanation += f"Hence, the patient's corrected concentration of sodium is {corrected_sodium} mEq/L.\n"

    return {"Explanation": explanation, "Answer": corrected_sodium, "Calculator Answer": compute_sodium_correction_hyperglycemia(input_variables)}



test_outputs = [
    {"sodium": [140.0, "mEq/L"], "glucose": [4.44, "mmol/L"]}, 
    {"sodium": [140.0, "mmol/L"], "glucose": [80.00, "mg/dL"]} 
      
]

outputs = ""
for i, test_case in enumerate(test_outputs):
    outputs += "Explanation:\n" +  compute_sodium_correction_hyperglycemia_explanation(test_case)["Explanation"] + "\n"


file_name = "explanations/sodium_correction_hyperglycemia.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)


with open(file_name, 'w') as file:
    file.write(outputs)