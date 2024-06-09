import json
import os
import anion_gap
import unit_converter_new
from rounding import round_number

def compute_albumin_corrected_anion(input_parameters):
     
    anion_gap_val = anion_gap.compute_anion_gap(input_parameters)
    albumin = unit_converter_new.conversions(input_parameters["albumin"][0], input_parameters["albumin"][1], "g/dL", None, None)

    return anion_gap_val + 2.5 * (4 - albumin)

def compute_albumin_corrected_anion_explanation(input_parameters):

    explanation = "The formula for computing a patient's albumin corrected anion gap is: anion_gap (in mEq/L) + 2.5 * (4 - albumin (in g/dL)).\n"

    anion_gap_data = anion_gap.compute_anion_gap_explanation(input_parameters)

    explanation += anion_gap_data["Explanation"]

    albumin_exp, albumin = unit_converter_new.conversion_explanation(input_parameters["albumin"][0], "albumin", None, None, input_parameters["albumin"][1], "g/dL")

    explanation += albumin_exp

    anion_gap_val = anion_gap_data["Answer"]
    answer = anion_gap_val + 2.5 * (4 - albumin) 
    final_answer = round_number(answer)

    explanation += f"Plugging in these values into the albumin corrected anion gap formula, we get {anion_gap_val} (mEq/L) + 2.5 * (4 - {albumin} (in g/dL)) = {final_answer} mEq/L. "
    explanation += f"Hence, the patient's albumin corrected anion gap is {final_answer} mEq/L.\n"

    return {"Explanation": explanation, "Answer": final_answer, "Calculator Answer": compute_albumin_corrected_anion(input_parameters)}


test_cases = [{"sodium": [140.02, "mmol/L"], "chloride": [100.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"], "albumin": [4.25, "g/dL"]},
             {"sodium": [112.03, "mmol/L"], "chloride": [90.02, "mmol/L"], "bicarbonate": [28.02, "mmol/L"], "albumin": [42.5, "g/L"]}]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_cases):
    outputs[i] = compute_albumin_corrected_anion_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/albumin_corrected_anion.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/albumin_corrected_anion.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)