import os
import json
import unit_converter_new
from rounding import round_number

def compute_ldl(input_parameters):

    total_cholestrol = unit_converter_new.conversions(input_parameters["total_cholestrol"][0], input_parameters["total_cholestrol"][1], "mg/dL", 386.654, None)
    hdl_cholestrol = unit_converter_new.conversions(input_parameters["hdl_cholestrol"][0], input_parameters["total_cholestrol"][1], "mg/dL", 386.654, None)
    triglycerides = unit_converter_new.conversions(input_parameters["triglycerides"][0], input_parameters["triglycerides"][1], "mg/dL", 861.338, None)

    return total_cholestrol - hdl_cholestrol - (triglycerides/5)


def compute_ldl_explanation(input_parameters):

    explanation = "To compute the patient's LDL cholestrol, apply the following formula: LDL cholesterol = total cholesterol - HDL - (triglycerides / 5), where the units for total cholestrol, HDL cholestrol, and triglycerides are all mg/dL.\n"

    total_cholestrol_exp, total_cholestrol = unit_converter_new.conversion_explanation(input_parameters["total_cholestrol"][0], "total cholestrol", 386.654, None, input_parameters["total_cholestrol"][1], "mg/dL")
    hdl_cholestrol_exp, hdl_cholestrol = unit_converter_new.conversion_explanation(input_parameters["hdl_cholestrol"][0], "hdl cholestrol", 386.654, None, input_parameters["hdl_cholestrol"][1], "mg/dL")
    triglycerides_exp, triglycerides = unit_converter_new.conversion_explanation(input_parameters["triglycerides"][0], "triglycerides", 861.338, None, input_parameters["triglycerides"][1], "mg/dL")

    explanation += total_cholestrol_exp + '\n'
    explanation += hdl_cholestrol_exp + '\n'
    explanation += triglycerides_exp +  '\n'

    answer = round_number(total_cholestrol - hdl_cholestrol - (triglycerides/5))

    explanation += f"Plugging in these values will give us {total_cholestrol} mg/dL - {hdl_cholestrol} mg/dL - ({triglycerides}/5) mg/dL = {answer} mg/dL.\n"

    explanation += f"The patients concentration of LDL cholestrol is {answer} mg/dL.\n"

    return {"Explanation": explanation, "Answer": answer, "Calculator Answer": compute_ldl(input_parameters)}

test_outputs = [{"total_cholestrol": [4.2, "mmol/L"], "hdl_cholestrol": [0.82, "mmol/L"], "triglycerides": [1.2, "mmol/L"]}, 
                {"total_cholestrol": [162.41, "mg/dL"], "hdl_cholestrol": [31.71, "mg/dL"], "triglycerides": [106.19, "mg/dL"]}
              ]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] =  compute_ldl_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/ldl.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/ldl.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
