import json
import os
import math
import unit_converter_new
import age_conversion
from rounding import round_number

def mdrd_gfr(input_variables):

    gender = input_variables["sex"]
    age = age_conversion.age_conversion(input_variables["age"])
    creatinine_conc = unit_converter_new.conversions(input_variables["creatinine"][0], input_variables["creatinine"][1], "mg/dL", 113.12, None)
   
    race_coefficient = 1

    if "race" in input_variables:
        race_coefficient = 1
        race = input_variables["race"]

        if race == "Black":
            race_coefficient = 1.212
        
    gender_coefficient = 1
    if gender == "Female":
        gender_coefficient =  0.742

    #print("age ", str(input_variables["age"]))
    #print("age conversion ", str(age))

    return 175 * creatinine_conc ** -1.154 * age ** -0.203 * race_coefficient * gender_coefficient


def mrdr_gfr_explanation(input_variables):
    gender = input_variables["sex"]


    age_explanation, age = age_conversion.age_conversion_explanation(input_variables["age"])
    creatinine_exp, creatinine_conc = unit_converter_new.conversion_explanation(input_variables["creatinine"][0], "Creatinine", 113.12, None, input_variables["creatinine"][1], "mg/dL")

    explanation = ""
    explanation += f"{age_explanation}"
    explanation += f"{creatinine_exp}\n"

    race_coefficient = 1

    if "race" in input_variables:
        race = input_variables["race"]
        if race == "Black":
            race_coefficient = 1.212
            explanation += "The patient is Black, so the race coefficient is 1.212.\n"
        else:
            explanation += "The patient is not Black, so the race coefficient is defaulted to 1.0.\n"
    else:
        explanation += "The race of the patient is not provided, so the default value of the race coefficient is 1.0.\n"

    gender_coefficient = 1
    if gender == "Female":
        gender_coefficient = 0.742
        explanation += "The patient is female, so the gender coefficient is 0.742.\n"
    else:
        explanation += "The patient is male, so the gender coefficient is 1.\n"

    gfr = round_number(175 * math.exp(math.log(creatinine_conc) * -1.154) * math.exp(math.log(age) * -0.203) * race_coefficient * gender_coefficient)


    explanation += (f"The patient's estimated GFR is calculated using the MDRD equation as:\n"
                    f"GFR = 175 * creatinine^(-1.154) * age^(-0.203) * race_coefficient * gender_coefficient. The creatinine concentration is mg/dL.\n"
                    f"Plugging in these values will give us: 175 * {creatinine_conc}^(-1.154) * {age}^(-0.203) * {race_coefficient} * {gender_coefficient}={gfr}.\n"
                    f"Hence, the patient's GFR is {gfr} mL/min/1.73m².\n")

    return {"Explanation": explanation, "Answer": gfr, "Calculator Answer": mdrd_gfr(input_variables)}


# Test cases for the GFR calculator
test_samples_gfr = [
    {"sex": "Male", "age": [50, "years"], "creatinine": [1.2, "mg/dL"], "race": "White"},  # Example with serum creatinine concentration in mg/dL
    {"sex": "Female", "age": [60, "years"], "creatinine": [60, "µmol/L"], "race": "Black"},  # Example with serum creatinine concentration in μmol/L
    {"sex": "Male", "age": [40, "years"], "creatinine": [0.8, "mg/dL"]},  # Example with different age and serum creatinine concentration
    {"sex": "Female", "age": [70, "years"], "creatinine": [0.6, "mg/dL"], "race": "Black"}  # Example with different age and serum creatinine concentration
]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_samples_gfr):
    outputs[i] =  mrdr_gfr_explanation(test_samples_gfr[i])
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/mean_arterial_pressure.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/mdrd_gfr.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

'''
Firstly, remove the last sentence from the USMLE quetions. 

'''