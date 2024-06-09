import os 
import json
import age_conversion

def compute_has_bled_score(input_variables):

    age_value = age_conversion.age_conversion(input_variables["age"])
    alcoholic_drinks_value = input_variables.get("alcoholic_drinks")
    hypertension_has_bled = input_variables.get("hypertension", False)
    liver_disease_value = input_variables.get("liver_disease_has_bled", False)
    renal_disease_value = input_variables.get("renal_disease_has_bled")
    stroke_history_value = input_variables.get("stroke", False)
    prior_bleeding_value = input_variables.get("prior_bleeding", False)
    labile_inr_value = input_variables.get("labile_inr", False)
    medications_for_bleeding_value = input_variables.get("medications_for_bleeding", False)

    has_bled_score = 0

    if age_value > 65:
        has_bled_score += 1

    if alcoholic_drinks_value >= 8:
        has_bled_score += 1

    if liver_disease_value: 
        has_bled_score += 1

    if hypertension_has_bled:
        has_bled_score += 1

    if renal_disease_value:
        has_bled_score += 1

    if stroke_history_value:
        has_bled_score += 1

    if prior_bleeding_value:
        has_bled_score += 1

    if labile_inr_value:
        has_bled_score += 1

    if medications_for_bleeding_value:
        has_bled_score += 1

    return has_bled_score


def compute_has_bled_score_explanation(input_variables):

    has_bled_score = 0

    num_alcolic_drinks = input_variables["alcoholic_drinks"]

    explanation = f"The current HAS-BLED score is 0.\n"
    age_explanation, age_value = age_conversion.age_conversion_explanation(input_variables["age"])
    explanation += age_explanation

    if age_value > 65:
        explanation += f"Because the patient's age is greater than 65 years, we increment the score by 1, making the current score {has_bled_score} + 1 = {has_bled_score + 1}.\n"
        has_bled_score += 1
    else:
        explanation += f"Because the patient's age is less than 66 years, we don't change the score, keeping the current score at {has_bled_score}.\n"


    if num_alcolic_drinks >= 8:
        explanation += f"The patient has {num_alcolic_drinks} drinks a week. Because the patient has at least 8 alcoholic drinks a week, we increment the score by 1, making the current score {has_bled_score} + 1 = {has_bled_score + 1}.\n"
        has_bled_score += 1
    else:
        explanation += f"The patient has {num_alcolic_drinks} drinks a week. Because the patient has less than 8 alcoholic drinks a week, we don't change the score, keeping the current score at {has_bled_score}.\n"

    default_parameters_set = {"hypertension": "hypertension", "liver_disease_has_bled":"liver disease", "renal_disease_has_bled":"renal disease", "stroke": "stroke history", "prior_bleeding": "prior bleeding", "labile_inr": "labile inr", "medications_for_bleeding": "medications for bleeding"}

    for parameter, name in default_parameters_set.items():

        if parameter not in input_variables:
            explanation += f"The issue, {name}, is missing from the patient note and so we assume it to be absent and so we do not change the score, keeping the current score at {has_bled_score}.\n"
            input_variables[parameter] = False
        elif not input_variables[parameter]:
            explanation += f"The issue, {name}, is reported to be absent for the patient and so we do not change the score, keeping the current score at {has_bled_score}.\n"
        else:
            explanation += f"The issue, {name}, is reported to be present for the patient note and so we increase the score by 1, making the current score {has_bled_score} + 1 = {has_bled_score + 1}.\n"
            has_bled_score += 1
            

    explanation += f"Hence, the patient's HAS-BLED score is {has_bled_score}.\n"

    return {"Explanation": explanation, "Answer": has_bled_score, "Calculator Answer": compute_has_bled_score(input_variables)}



test_outputs = [{"age": [45, "years"], 
                 "alcoholic_drinks": 8, 
                 "liver_disease_has_bled": True, 
                 "renal_disease_has_bled": False, 
                 "stroke": False, 
                 "prior_bleeding": True,
                 "hypertension_has_bled": True, 
                 "labile_inr": False, 
                 "medications_for_bleeding": False}, 

                 {"age": [15, "years"], 
                 "alcoholic_drinks": 2, 
                 "liver_disease_has_bled": True, 
                 "stroke": False, 
                 "hypertension_has_bled": True}, 

                 {"age": [75, "years"], 
                 "alcoholic_drinks": 10, 
                 "liver_disease_has_bled": True, 
                 "renal_disease_has_bled": False, 
                 "prior_bleeding": True,
                 "medications_for_bleeding": False}
                 
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_has_bled_score_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/has_bled_score.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/has_bled_score.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
