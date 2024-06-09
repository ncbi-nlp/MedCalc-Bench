import os
import json 
import age_conversion
import unit_converter_new
from rounding import round_number

def ckd_epi_2021(input_parameters):

    age = age_conversion.age_conversion(input_parameters["age"])
    gender = input_parameters["sex"]
    creatinine_val, creatinine_label = input_parameters["creatinine"][0], input_parameters["creatinine"][1]
    creatinine_val = unit_converter_new.conversions(creatinine_val, creatinine_label, "mg/dL", 113.12, None)

    if creatinine_val <= 0.7 and gender == "Female":
        a = 0.7
        b = -0.241

    elif creatinine_val <= 0.9 and gender == "Male":
        a = 0.7
        b = -0.302

    elif creatinine_val > 0.7 and gender == "Female":
            a = 0.7
            b = -1.2

    elif creatinine_val > 0.9 and gender == "Male":
            a = 0.9
            b = -1.2

    if gender == "Female":
        gender_coefficient = 1.012 
    else:
        gender_coefficient = 1 

    return 142 * (creatinine_val/a)**b * 0.9938**age * gender_coefficient

def ckd_epi_2021_explanation(input_parameters):

    explanation = "The formula for computing GFR is 142 x (Scr/A)**B x 0.9938**age x (gender_coeffcient), where the ** indicates an exponent operation, Scr is the concentration of serum creatinine in mg/dL and gender_coefficient is 1.012 if the patient is female, else the coeffient is 1. The coefficients A and B are dependent on the patient's gender and the patient's creatinine concentration.\n"

    age_explanation, age = age_conversion.age_conversion_explanation(input_parameters["age"])
    gender = input_parameters["sex"]

    explanation += age_explanation
    explanation += f"The patient's gender is {gender}, "

    if gender == "Female":
        gender_coefficient = 1.012 
        explanation += f"and so the patient's gender coefficient is {gender_coefficient}.\n"
    else:
        gender_coefficient = 1.000
        explanation += f"and so the patient's gender coefficient is {gender_coefficient}.\n"

    creatinine_val, creatinine_label = input_parameters["creatinine"][0], input_parameters["creatinine"][1]
    creatinine_val_exp, creatinine_val = unit_converter_new.conversion_explanation(creatinine_val, "Serum Creatinine", 113.12, None, creatinine_label, "mg/dL")

    explanation += creatinine_val_exp

    if creatinine_val <= 0.7 and gender == "Female":
        explanation += f"Because the patient's gender is female and the creatinine concentration is less than or equal to 0.7 mg/dL, A = 0.7 and B = -0.241.\n"
        a = 0.7
        b = -0.241

    elif creatinine_val <= 0.9 and gender == "Male":
        explanation += f"Because the patient's gender is male and the creatinine concentration is less than or equal to 0.9 mg/dL, A = 0.7 and B = -0.302.\n"
        a = 0.7
        b = -0.302

    elif creatinine_val > 0.7 and gender == "Female":
        explanation += f"Because the patient's gender is female and the creatinine concentration is greater than or equal to 0.7 mg/dL, A = 0.7 and B = -1.2.\n"
        a = 0.7
        b = -1.2

    elif creatinine_val > 0.9 and gender == "Male":
        explanation += f"Because the patient's gender is male and the creatinine concentration is greater than or equal to 0.9 mg/dL, A = 0.9 and B = -1.2.\n"
        a = 0.9
        b = -1.2


    result = round_number(142 * (creatinine_val/a)**b * 0.9938**age * gender_coefficient)

    explanation += f"Plugging in these values, we get 142 * ({creatinine_val}/{a})**{b} * {0.9938}**{age} * {gender_coefficient} = {result}.\n"
    explanation += f"Hence, the GFR value is {result} ml/min/1.73 m².\n"

    return {"Explanation": explanation, "Answer": result, "Calculator Answer": ckd_epi_2021(input_parameters)}
 


test_outputs = [{"age": [50, "years"], 
                 "sex": "Male",
                 "creatinine": [90, "µmol/L"]}, 

                {"age": [50, "years"], 
                 "sex": "Female",
                 "creatinine": [1.2, "mg/dL"]}, 

                {"age": [50, "years"], 
                 "sex": "Female",
                 "creatinine": [90, "µmol/L"]}, 
                
                {"age": [50, "years"], 
                 "sex": "Female",
                 "creatinine": [1.2, "mg/dL"]}, 

                {"age": [45, "years"], "creatinine": [1.5, "mg/dL"], "sex": "Female"} ,
                {"age": [35, "years"], "creatinine": [106.08, "µmol/L"], "sex": "Male"}
                 
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = ckd_epi_2021_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/ckd-epi.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/ckd-epi.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

