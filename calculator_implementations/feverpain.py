import json
import os 


def compute_fever_pain(input_parameters):

    fever_pain_score = 0

    fever_24_hours = input_parameters.get("fever_24_hours", False)
    cough_coryza_absent =  input_parameters.get("cough_coryza_absent", False)
    symptom_onset = input_parameters.get("symptom_onset", False)
    purulent_tonsils = input_parameters.get("purulent_tonsils", False)
    severe_tonsil_inflammation = input_parameters.get("severe_tonsil_inflammation", False)

    if fever_24_hours:
        fever_pain_score += 1
    
    if cough_coryza_absent:
        fever_pain_score += 1
    
    if symptom_onset:
        fever_pain_score += 1
    
    if purulent_tonsils:
        fever_pain_score += 1
    
    if severe_tonsil_inflammation:
        fever_pain_score += 1

    return fever_pain_score

def compute_fever_pain_explanation(input_parameters):

    parameter_name = {"fever_24_hours": "a fever in the past 24 hours", "cough_coryza_absent": "an absence of cough or coryza", 
                      "symptom_onset": "a symptom onset ≤3 days", "purulent_tonsils": "purulent tonsils", "severe_tonsil_inflammation": "severe tonsil inflammation"}
    
    fever_pain_score = 0

    explanation = "The patient's current FeverPain score is 0.\n"

    for parameter in parameter_name:

        if parameter not in input_parameters:
            explanation += f"Whether the patient has {parameter_name[parameter]} is not reported and so we assume that it is absent for the patient. Because of this, we do not increment the score, keeping the current total at {fever_pain_score}.\n"
        
        elif input_parameters[parameter]:
            explanation += f"'The patient is reported to have {parameter_name[parameter]} and so we increment the score by 1, making the current total {fever_pain_score} + 1 = {fever_pain_score + 1}.\n"
            fever_pain_score += 1

        else:
            explanation += f"The patient is reported to not have {parameter_name[parameter]} and so we do not increment the score, keeping the current total at {fever_pain_score}.\n"

    explanation += f"The patient's FeverPain score is {fever_pain_score} points.\n"

    return {"Explanation": explanation, "Answer": fever_pain_score, "Calculator Answer": compute_fever_pain(input_parameters)}



test_outputs = [ {"fever_24_hours": True, "cough_coryza_absent": True, "symptom_onset": True, 
                  "purulent_tonsils": True, "severe_tonsil_inflammation": True}, 

                 {"fever_24_hours": False, "cough_coryza_absent": False, "symptom_onset": False, 
                  "purulent_tonsils": False, "severe_tonsil_inflammation": False}, 
                  
                  {}
                  ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_fever_pain_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/feverpain.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/feverpain.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)

