import os 
import json 
import unit_converter_new
from rounding import round_number


def compute_steroid_conversion(input_parameters):

    conversion_dict = {"Betamethasone IV": 1, 
                    "Cortisone PO": 33.333, 
                    "Dexamethasone IV": 1, 
                    "Dexamethasone PO": 1,
                    "Hydrocortisone IV": 26.667,
                    "Hydrocortisone PO": 26.667,
                    "MethylPrednisoLONE IV": 5.333,
                    "MethylPrednisoLONE PO": 5.333,
                    "PrednisoLONE PO": 6.667, 
                    "PredniSONE PO": 6.667, 
                    "Triamcinolone IV": 5.333
                }
    
    input_drug_mass = unit_converter_new.conversions(input_parameters["input steroid"][1], input_parameters["input steroid"][2], "mg", None, None)
    
    target_drug_name = input_parameters["target steroid"]
    input_drug_name = input_parameters["input steroid"][0]


    from_multiplier = conversion_dict[input_drug_name]
    to_multiplier = conversion_dict[target_drug_name]
    conversion_factor = (to_multiplier / from_multiplier)
    converted_amount = input_drug_mass * (conversion_factor)
    return converted_amount

def compute_steroid_conversion_explanation(input_parameters):


    conversion_dict = {"Betamethasone IV": 1, 
                    "Cortisone PO": 33.33, 
                    "Dexamethasone IV": 1, 
                    "Dexamethasone PO": 1,
                    "Hydrocortisone IV": 26.67,
                    "Hydrocortisone PO": 26.67,
                    "MethylPrednisoLONE IV": 5.33,
                    "MethylPrednisoLONE PO": 5.33,
                    "PrednisoLONE PO": 6.67, 
                    "PredniSONE PO": 6.67, 
                    "Triamcinolone IV": 5.33
                }
    
    explanation = ""
    input_drug_mass_exp, input_drug_mass = unit_converter_new.conversion_explanation(input_parameters["input steroid"][1], input_parameters["input steroid"][0], None, None, input_parameters["input steroid"][2], "mg")
    explanation += input_drug_mass_exp

    target_drug_name = input_parameters["target steroid"]
    input_drug_name = input_parameters["input steroid"][0]
    input_unit = input_parameters["input steroid"][2]


    from_multiplier = conversion_dict[input_drug_name]
    to_multiplier = conversion_dict[target_drug_name]

    from_multiplier = conversion_dict[input_drug_name]
    to_multiplier = conversion_dict[target_drug_name]
    
    conversion_factor = round_number(to_multiplier / from_multiplier)
    converted_amount = round_number(input_drug_mass * conversion_factor)
    input_drug_mass = round_number(input_drug_mass)

    explanation += f"To convert from the {input_drug_name} to {target_drug_name}, multiply by the conversion factor, {conversion_factor} mg {target_drug_name}/{input_drug_name}, giving us {input_drug_mass} mg {input_drug_name} * {conversion_factor} mg {target_drug_name}/mg {input_drug_name} = {converted_amount} mg {target_drug_name}. "
    
    explanation += f"{input_drug_mass} {input_unit} of {input_drug_name} is equal to {converted_amount} mg of {target_drug_name}.\n"
    

    return {"Explanation": explanation, "Answer": converted_amount, "Calculator Answer": compute_steroid_conversion(input_parameters)}


test_cases = [{"input steroid": ["PredniSONE PO", 2, "mg"], "target steroid": "PrednisoLONE PO"}, {"input steroid": ["PredniSONE PO", 0.1, "g"], "target steroid": "Hydrocortisone IV"}]

outputs = ""

for i in range(len(test_cases)):
    outputs += "Explanations:\n" + compute_steroid_conversion_explanation(test_cases[i])["Explanation"] + "\n"


file_name = "explanations/steroid_conversion_explanation.txt"

with open(file_name, 'w') as file:
    file.write(outputs)
