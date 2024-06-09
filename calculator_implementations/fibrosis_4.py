import os
import json
import math 
import unit_converter_new
import age_conversion
from rounding import round_number

def compute_fib4(input_parameters):

    age = age_conversion.age_conversion(input_parameters["age"])

    ast_value = input_parameters["ast"][0]

    alt_value = input_parameters["alt"][0]

    # be sure to convert to liter
    platelet_count = unit_converter_new.convert_to_units_per_liter(input_parameters["platelet_count"][0], input_parameters["platelet_count"][1], "L")

    return (age * ast_value) / ( (platelet_count/(1e9)) * math.sqrt(alt_value) )


def compute_fib4_explanation(input_parameters):

    explanation = ""

    age_explanation, age = age_conversion.age_conversion_explanation(input_parameters["age"])
    explanation += age_explanation

    ast_value = input_parameters["ast"][0]
    alt_value = input_parameters["alt"][0]
    src_value = input_parameters["platelet_count"][0]
    src_unit = input_parameters["platelet_count"][1]
    explanation = f"The formula for computing Fibrosis-4 is Fib-4 = (Age * AST) / (Platelet count (in billions) * √ALT), where platelet count is the number of billions per L, and the units for AST and ALT are both U/L.\n"

    explanation_platelet, platelet_value = unit_converter_new.convert_to_units_per_liter_explanation(src_value, src_unit, "platelets", "L")

    count_platelet_billions = platelet_value/(1e9)
    result = round_number((age * ast_value)/(count_platelet_billions * math.sqrt(alt_value)))

    explanation += f"The patient's concentration of AST is {ast_value} U/L.\n"
    explanation +=  f"The patient's concentration of ALT is {alt_value} U/L.\n"

    explanation += f"{explanation_platelet}This means that there are {platelet_value}/(10^9) = {count_platelet_billions} billion platelet counts per liter.\n"
    explanation += f"Plugging these values into the formula, we get ({age} * {ast_value})/({count_platelet_billions} * sqrt({alt_value})) = {result}.\n"
    explanation += f"Hence, the Fibrosis-4 score is {result}."
    
    return {"Explanation": explanation, "Answer": result, "Calculator Answer": compute_fib4(input_parameters)}


test_outputs = [
    {
        'age': [40, 'years'],
        'ast': [26, 'U/L'],
        'alt': [17, 'U/L'],
        'platelet_count': [1.5e11, "L"],
    },
    {
        'age': [40, 'years'],
        'ast': [26, 'U/L'],
        'alt': [17, 'U/L'],
        'platelet_count': [1.5e5, "µL"],
    },
    
]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_fib4_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"


'''
file_name = "explanations/fib-4.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/fib-4.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)





