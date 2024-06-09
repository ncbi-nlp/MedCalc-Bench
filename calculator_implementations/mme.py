import json
import os
import unit_converter_new
from rounding import round_number

def compute_mme(input_parameters):

    mme_drug = {"Codeine": 0.15, 
            "FentaNYL buccal": 0.13,
            "FentANYL patch": 2.4,
            "HYDROcodone": 1,
            "HYDROmorphone": 5,
            "Methadone": 4.7, 
            "Morphine": 1, 
            "OxyCODONE": 1.5, 
            "OxyMORphone": 3, 
            "Tapentadol": 0.4, 
            "TraMADol": 0.2, 
            "Buprenorphine": 10}
    
    mme_equivalent = 0
    
    for drug_name in input_parameters:
        if "Day" in drug_name:
            continue 

        name = drug_name.split(" Dose")[0]

        if name == "FentaNYL buccal" or name == "FentANYL patch":
            drug_mass = unit_converter_new.conversions(input_parameters[name + " Dose"][0], input_parameters[name + " Dose"][1], "µg", None, None)

        
        drug_mass = unit_converter_new.conversions(input_parameters[name + " Dose"][0], input_parameters[name + " Dose"][1], "mg", None, None)

        dose_per_day_key = name + " Dose Per Day"

        dose_per_day = input_parameters[dose_per_day_key][0]

        mme_equivalent += dose_per_day * mme_drug[name] * drug_mass
        
    return mme_equivalent
    

def mme_explanation(input_parameters):

    explanation = "The curent Morphine Milligram Equivalents (MME) is 0 MME per day.\n"
    
    mme_drug = {"Codeine": 0.15, 
            "FentaNYL buccal": 0.13,
            "FentANYL patch": 2.4,
            "HYDROcodone": 1,
            "HYDROmorphone": 5,
            "Methadone": 4.7, 
            "Morphine": 1, 
            "OxyCODONE": 1.5, 
            "OxyMORphone": 3, 
            "Tapentadol": 0.4, 
            "TraMADol": 0.2, 
            "Buprenorphine": 10}
    
    mme_equivalent = 0
    
    for drug_name in input_parameters:
        if "Day" in drug_name:
            continue 

        name = drug_name.split(" Dose")[0]

        units = input_parameters[name + " Dose"][1]


        if name != "FentaNYL buccal" and name != "FentaNYL patch":
            drug_mg_exp, drug_mg = unit_converter_new.conversion_explanation(input_parameters[name + " Dose"][0], name, None, None, units, "mg")
            if units == "mg":
                explanation += f"The patient's dose of {name} is {drug_mg} mg. "
            else:
                explanation += f"The patient's dose of {name} is measured in {units}. We need to convert this to mg. "
                explanation += drug_mg_exp + "\n"
        else:
            drug_mg_exp, drug_mg = unit_converter_new.conversion_explanation(input_parameters[name + " Dose"][0], name, None, None, units, "µg")
            if units == "µg":
                explanation += f"The patient's dose of {name} is {drug_mg} µg.\n"
            else:
                explanation += f"The patient's dose of {name} is measured in {units}. We need to convert this to µg. "
                explanation += drug_mg_exp + "\n"


        target_unit = "mg" if name != "FentaNYL buccal" and name != "FentaNYL patch" else "µg"

        dose_per_day_key = name + " Dose Per Day"

        dose_per_day = input_parameters[dose_per_day_key][0]

        total_per_day = round_number(drug_mg * dose_per_day)

        explanation += f"The patient takes {dose_per_day} doses/day of {name}. This means that the patient takes {round_number(drug_mg)} {target_unit}/dose {name} * {dose_per_day} dose/day = {total_per_day} {target_unit}/day. "

        explanation += f"To convert to mme/day of {name}, multiply the {total_per_day} {target_unit}/day by the mme conversion factor, {mme_drug[name]} mme/{target_unit}, giving us {round_number(mme_drug[name] * total_per_day)} mme/day. "
    
        explanation += f"Adding the mme/day of {name} to the total mme/day gives us {round_number(mme_equivalent)} + {round_number(mme_drug[name] * total_per_day)} = {round_number(mme_equivalent + mme_drug[name] * total_per_day)} mme/day.\n"

        mme_equivalent += dose_per_day * mme_drug[name] * drug_mg

        mme_equivalent = round_number(mme_equivalent)


    explanation += f"The patient's mme/day is {mme_equivalent} mme/day."
        
    return {"Explanation": explanation, "Answer": mme_equivalent, "Calculator Answer": compute_mme(input_parameters)}


test_cases = [{"Codeine Dose": [15, "mg"],
               "Codeine Dose Per Day": [2, "per day"],
               "FentaNYL buccal Dose": [100, "µg"],
               "FentaNYL buccal Dose Per Day": [1, "per day"]}, 

               {"HYDROcodone Dose": [15, "mg"],
               "HYDROcodone Dose Per Day": [2, "per day"],
               "HYDROmorphone Dose": [100, "mg"],
               "HYDROmorphone Dose Per Day": [1, "per day"], 
               "Methadone Dose": [25, "mg"],
               "Methadone Dose Per Day": [3, "per day"]},

               {"Morphine Dose": [15, "mg"],
               "Morphine Dose Per Day": [2, "per day"],
               "OxyCODONE Dose": [100, "mg"],
               "OxyCODONE Dose Per Day": [1, "per day"], 
               "OxyMORphone Dose": [25, "mg"],
               "OxyMORphone Dose Per Day": [3, "per day"]},

               {"Tapentadol Dose": [15, "mg"],
               "Tapentadol Dose Per Day": [2, "per day"],
               "TraMADol Dose": [100, "mg"],
               "TraMADol Dose Per Day": [1, "per day"]}]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_cases):
    outputs[i] = mme_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"


file_name = "/Users/khandekarns/Documents/GSM8k-Med/calculator_implementations/explanations/mme.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)



file_name = "explanations/mme.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)