import os
import json 
import anion_gap
from rounding import round_number

def compute_delta_gap(input_parameters):

    anion_gap_val = anion_gap.compute_anion_gap(input_parameters)

    return  anion_gap_val - 12.0

def compute_delta_gap_explanation(input_parameters):

    explanation = f"To compute the formula of the delta gap, the formula is anion gap (in mEq/L) - 12. The first step is to compute the patient's anion gap.\n"

    anion_gap_resp = anion_gap.compute_anion_gap_explanation(input_parameters)

    explanation += anion_gap_resp["Explanation"]

    anion_gap_val = anion_gap_resp["Answer"]

    answer = round_number(anion_gap_val - 12.0)

    explanation += f"Plugging in {anion_gap_val} mEq/L for the delta gap formula, we get {anion_gap_val} - 12 = {answer} mEq/L. "
    explanation += f"Hence, the patient's delta gap is {answer} mEq/L.\n"

    return {"Explanation": explanation, "Answer": answer, "Calculator Answer": compute_delta_gap(input_parameters) }

test_cases = [{"sodium": [140.02, "mmol/L"], "chloride": [100.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"]},
             {"sodium": [112.03, "mmol/L"], "chloride": [90.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"]}]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_cases):
    outputs[i] = compute_delta_gap_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/delta_gap.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/delta_gap.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
