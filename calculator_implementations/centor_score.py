import json
import os
import convert_temperature
import age_conversion

def compute_centor_score(input_parameters):

    centor_score = 0
    
    age = age_conversion.age_conversion(input_parameters["age"])
    temperature, temp_units = input_parameters["temperature"][0], input_parameters["temperature"][1]

    temperature = convert_temperature.fahrenheit_to_celsius(temperature, temp_units)
    
    cough_absent_value = input_parameters.get("cough_absent", True)
    tender_lymph_nodes_value = input_parameters.get("tender_lymph_nodes", False)
    swelling_tonsils_value = input_parameters.get("exudate_swelling_tonsils", False)

    if 3 <= age <= 14:
        centor_score += 1 
    elif age >= 45:
        centor_score = -1    

    if cough_absent_value:
        centor_score += 1

    if tender_lymph_nodes_value:
        centor_score += 1
   
    if swelling_tonsils_value:
        centor_score += 1

    if temperature > 38:
        centor_score += 1
        
    return centor_score

def compute_centor_score_explanation(input_variables):
   
    centor_score = 0
    age_explanation, age = age_conversion.age_conversion_explanation(input_variables["age"])
    explanation = f"The current Centor score is 0.\n"
    explanation += age_explanation

    if 3 <= age <= 14:
        explanation += f"Because the age is between 3 and 14 years, we add one point to the score making current score {centor_score} + 1 = {centor_score + 1}.\n"
        centor_score += 1
    elif 15 <= age <= 44:
        explanation += f"Because the age is in between 15 and 44 years, the score does not change, keeping the score at {centor_score}.\n"
    elif age >= 45:
        explanation +=  f"Because the age is greater than 44 years, we decrease the score by one point, making the score {centor_score} - 1 = {centor_score - 1}.\n"
        centor_score -= 1

    explanation_temp, temp_val = convert_temperature.fahrenheit_to_celsius_explanation(input_variables["temperature"][0], input_variables["temperature"][1])

    explanation += explanation_temp
    if temp_val > 38:
        explanation += f"The patient's temperature is greater than 38 degrees Celsius, and so we add one point to the score, making the current score {centor_score} + 1 = {centor_score + 1}.\n"
        centor_score += 1
    elif temp_val <= 38:
        explanation += f"The patient's temperature is less than or equal to 38 degrees Celsius, and so we do not make any changes to the score, keeping the score at {centor_score}.\n"

    default_parameters_dict = {"cough_absent": "cough absent", "tender_lymph_nodes": "tender/swollen anterior cervical lymph nodes", "exudate_swelling_tonsils": "exudate or swelling on tonsils"}

    for parameter in default_parameters_dict:

        if parameter not in input_variables:
            explanation += f"The patient note does not mention details about '{default_parameters_dict[parameter]}' and so we assume it to be absent. "
            input_variables[parameter] = False
            explanation += f"Hence, we do not change the score, keeping the current score at {centor_score}.\n"
        elif not input_variables[parameter]:
            explanation += f"The patient note reports '{default_parameters_dict[parameter]}' as absent for the patient. Hence, we do not change the score, keeping the current score at {centor_score}.\n"
        else:
            explanation += f"The patient note reports '{default_parameters_dict[parameter]}' as present for the patient. Hence, we increase the score by 1, making the current score {centor_score} + 1 = {centor_score + 1}.\n"
            centor_score += 1
            

    explanation += f"Hence, the Centor score for the patient is {centor_score}.\n"

    return {"Explanation": explanation, "Answer": centor_score, "Calculator Answer": compute_centor_score(input_variables)}


test_outputs = [{"age": [45, "years"], 
                "temperature": [102, "degrees fahreinheit"],
                "cough_absent": True, 
                "tender_lymph_nodes": False,
                "exudate_swelling_tonsils": True
                }, 

                {"age": [43, "years"], 
                "temperature": [40, "degrees celsius"],
                "cough_absent": True, 
                "exudate_swelling_tonsils": True
                }, 

                {"age": [50, "years"], 
                "temperature": [40, "degrees celsius"],
                "cough_absent": True, 
                "tender_lymph_nodes": False,
                }]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_centor_score_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/centor_score.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/centor_score.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)