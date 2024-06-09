import os
import json
import unit_converter_new
from rounding import round_number

def calculate_corrected_calcium(params):

    normal_albumin = 4.0 # Normal albumin level in g/dL
    albumin = params.get('albumin')
    albumin_val = albumin[0]
    albumin_units = albumin[1]
    calcium = params.get('calcium')
    calcium_val = calcium[0]
    calcium_units = calcium[1]

    albumin_val = unit_converter_new.conversions(albumin_val, albumin_units, "g/dL", 66500, None)
    calcium_val = unit_converter_new.conversions(calcium_val, calcium_units, "mg/dL", 40.08, 2)

    corrected_calcium = (0.8 * (normal_albumin - albumin_val)) + calcium_val

    return corrected_calcium


def calculate_corrected_calcium_explanation(params):

    # Extract parameters from the input dictionary
    normal_albumin = 4.0  # Normal albumin level in g/dL
    
    albumin = params.get('albumin')
    albumin_val = albumin[0]
    albumin_units = albumin[1]

    calcium = params.get('calcium')
    calcium_val = calcium[0]
    calcium_units = calcium[1]

    output = f"To compute the patient's correct calcium level in mg/dL, the formula is  (0.8 * (Normal Albumin (in g/dL) - Patient's Albumin (in g/dL))) + Serum Calcium (in mg/dL).\n"


    # Generate explanation
    output += "The patient's normal albumin level is 4.0 g/dL.\n"
    albumin_explanation, albumin  = unit_converter_new.conversion_explanation(albumin_val, "Albmumin", 66500, None, albumin_units, "g/dL" )
    calcium_explanation, calcium  = unit_converter_new.conversion_explanation(calcium_val, "Calcium", 40.08, 2, calcium_units, "mg/dL")

    output += f"{albumin_explanation}\n"
    output += f"{calcium_explanation}\n"

    corrected_calcium = round_number(0.8 * (normal_albumin - albumin) + calcium)

    output += f"Plugging these values into the formula, we get "
    output += f"(0.8 * ({normal_albumin} g/dL - {albumin} g/dL)) + {calcium} mg/dL = {corrected_calcium} mg/dL.\n"


    output += f"The patient's corrected calcium concentration {corrected_calcium} mg/dL.\n"

    return {"Explanation": output, "Answer": corrected_calcium, "Calculator Answer": calculate_corrected_calcium(params)}


output = {}


test_outputs = [{"albumin": [3.00, "g/dL"], 
                 "calcium": [10.0, "mg/dL"]}, 

                 {"albumin": [30.0, "g/L"], 
                 "calcium": [2.50, "mmol/L"]}
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = calculate_corrected_calcium_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/calcium_correction.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/calcium_correction.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

   