import os
import json 
import albumin_corrected_anion
from rounding import round_number


def compute_albumin_corrected_delta_gap(input_parameters):

    albumin_corrected_val = albumin_corrected_anion.compute_albumin_corrected_anion(input_parameters)

    return albumin_corrected_val - 12.0

def compute_albumin_corrected_delta_gap_explanation(input_parameters):

    explanation = f"To compute the formula of albumin corrected delta gap, the formula is albumin corrected anion gap (in mEq/L) - 12.\n"

    albumin_corrected_resp = albumin_corrected_anion.compute_albumin_corrected_anion_explanation(input_parameters)

    explanation += albumin_corrected_resp["Explanation"]

    albumin_corrected_val = albumin_corrected_resp["Answer"]

    answer = round_number(albumin_corrected_val - 12.0)

    explanation += f"Plugging in {albumin_corrected_val} mEq/L for the anion gap into the albumin corrected delta gap formula, we get {albumin_corrected_val} - 12 = {answer} mEq/L. "
    explanation += f"Hence, the patient's albumin corrected delta gap is {answer} mEq/L.\n"

    return {"Explanation": explanation, "Answer": answer, "Calculator Answer": compute_albumin_corrected_delta_gap(input_parameters) }

test_cases = [{"sodium": [140.02, "mmol/L"], "chloride": [100.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"], "albumin": [4.25, "g/dL"]},
             {"sodium": [112.03, "mmol/L"], "chloride": [90.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"], "albumin": [42.5, "g/L"]}]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_cases):
    outputs[i] = compute_albumin_corrected_delta_gap_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/albumin_corrected_delta_gap.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/albumin_corrected_delta_gap.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)