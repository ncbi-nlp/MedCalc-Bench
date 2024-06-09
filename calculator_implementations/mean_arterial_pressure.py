import json
import os
from rounding import round_number


def calculate_map(variables):
    sys_bp = variables['sys_bp'][0]
    dia_bp = variables['dia_bp'][0]


    return 2*dia_bp/3 + sys_bp/3

def mean_arterial_pressure_explanation(variables):

    print(variables['sys_bp'])
    print(variables['dia_bp'])


    sys_bp = variables['sys_bp']
    dia_bp = variables['dia_bp']
    
    output = ""

    value = round_number(2*dia_bp[0]/3 + sys_bp[0]/3)

    output += f"The mean average pressure is computed by the formula 2/3 * (diastolic blood pressure) + 1/3 * (systolic blood pressure). Plugging in the values, we get 2/3 * {dia_bp[0]} mm Hg + 1/3 * {sys_bp[0]} mm Hg = {value} mm Hg.\n"
    output += f"Hence, the patient's mean arterial pressure is {value} mm Hg.\n"

    return {"Explanation": output, "Answer": value, "Calculator Answer": calculate_map(variables)}

'''
outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] =  mean_arterial_pressure_explanation(test_outputs[i])
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"


file_name = "explanations/mean_arterial_pressure.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)



file_name = "explanations/mean_arterial_pressure.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
'''