import os
import json 
import unit_converter_new


def compute_cardiac_index(input_variables):

    elevated_risk_surgery = input_variables.get('elevated_risk_surgery', False)
    ischemetic_heart_disease = input_variables.get('ischemetic_heart_disease', False)
    congestive_heart_failure = input_variables.get('congestive_heart_failure', False)
    cerebrovascular_disease = input_variables.get('cerebrovascular_disease', False)
    pre_operatative_insulin_treatment = input_variables.get('pre_operative_insulin_treatment', False)
    
    # make sure to convert units for this one to mg/dL 
    pre_operative_creatinine = unit_converter_new.conversions(input_variables['pre_operative_creatinine'][0], input_variables['pre_operative_creatinine'][1], "mg/dL", 113.12, None)

    elevated_risk_surgery_score = 0
    ischemetic_heart_disease_score = 0
    congestive_heart_failure_score = 0
    cerebrovascular_disease_score = 0
    pre_operatative_insulin_treatment_score = 0
    pre_operative_creatinine_score = 0

    
    if elevated_risk_surgery:
        elevated_risk_surgery_score += 1
    if ischemetic_heart_disease:
        ischemetic_heart_disease_score += 1
    if congestive_heart_failure:
        congestive_heart_failure_score += 1
    if cerebrovascular_disease: 
        cerebrovascular_disease_score += 1
    if pre_operatative_insulin_treatment:
        pre_operatative_insulin_treatment_score += 1
    if pre_operative_creatinine > 2:
        pre_operative_creatinine_score += 1

    
    return elevated_risk_surgery_score + ischemetic_heart_disease_score + congestive_heart_failure_score + cerebrovascular_disease_score + pre_operatative_insulin_treatment_score + pre_operative_creatinine_score



def compute_cardiac_index_explanation(input_variables):
    # List of parameters and their default values
    parameters = {
        'elevated_risk_surgery': "elevated risk surgery",
        'ischemetic_heart_disease': "ischemetic heart disease",
        'congestive_heart_failure': "congestive heart failure", 
        'cerebrovascular_disease': "cerebrovascular disease",
        'pre_operative_insulin_treatment': "pre-operative insulin treatment",
        'pre_operative_creatinine': "pre-operative creatinine" 
    }
    

    # Initializing scores and output explanation
    cri = 0
    output = "The current cardiac risk index is 0.\n"
    #output += "Total Score = elevated_risk_surgery_score + ischemetic_heart_disease_score + congestive_heart_failure_score + cerebrovascular_disease_score + pre_operative_insulin_treatment_score + pre_operative_creatinine_score.\n\n"    

    for param_name, full_name in parameters.items():
        param_value = input_variables.get(param_name)

        # If parameter is missing, assume it as False
        if param_value is None:
            output += f"The patient note does not mention about {full_name} and is assumed to be absent. "
            input_variables[param_name] = False
            param_value = False
        elif param_name != 'pre_operative_creatinine':
            value = 'absent' if not param_value else 'present'
            output += f"The patient note reports {full_name} as '{value}' for the patient. "
        elif param_name == 'pre_operative_creatinine':
            explanation, param_value = unit_converter_new.conversion_explanation(param_value[0], "Pre-Operative Creatinine", 113.12, None, param_value[1], "mg/dL" )
            input_variables['pre_operative_creatinine'] = [param_value, "mg/dL"]
            output += explanation
          
        if param_name == 'pre_operative_creatinine':

            if param_value > 2: 
                output += f"The patient has pre-operative creatinine > 2 mg/dL, so we increment the score by one and the current total will be {cri} + 1 = {cri + 1}.\n"
                cri += 1
            else:
                output += f"The patient has pre-operative creatinine <= 2 mg/dL, so we keep the score the same at {cri}.\n"
            continue

        if param_value:
            output += f"This means that we increment the score by one and the current total will be {cri} + 1 = {cri + 1}.\n"
            cri += 1
        else:
            output += f"This means that the total score remains unchanged at {cri}.\n"


    output += f"\nThe cardiac risk index score is {cri}.\n"

    return {"Explanation": output, "Answer": cri, "Calculator Answer": compute_cardiac_index(input_variables)}


test_outputs = [
    {
        'elevated_risk_surgery': True,
        'ischemetic_heart_disease': False,
        'congestive_heart_failure': True,
        'pre_operative_insulin_treatment': False,
        'pre_operative_creatinine': [1.5, "mg/dL"]
    },
    {
        'elevated_risk_surgery': False,
        'ischemetic_heart_disease': True,
        'congestive_heart_failure': False,
        'pre_operative_insulin_treatment': True,
        'pre_operative_creatinine': [2.5, "mg/dL"]
    },
    {
        'elevated_risk_surgery': True,
        'ischemetic_heart_disease': True,
        'congestive_heart_failure': True,
        'cerebrovascular_disease': True,
        'pre_operative_insulin_treatment': False,
        'pre_operative_creatinine': [3.0, "mg/dL"]
    },
    {
        'elevated_risk_surgery': False,
        'ischemetic_heart_disease': False,
        'cerebrovascular_disease': False,
        'pre_operative_insulin_treatment': False,
        'pre_operative_creatinine': [1.8, "mg/dL"]
    }
]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_cardiac_index_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/cri.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/cri.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
