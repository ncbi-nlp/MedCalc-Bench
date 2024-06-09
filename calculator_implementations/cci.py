import os
import json
import age_conversion

def compute_cci(input_parameters):

    age = age_conversion.age_conversion(input_parameters["age"])
    mi = input_parameters.get("mi", False)
    chf = input_parameters.get("chf", False)
    peripheral_vascular_disease = input_parameters.get("peripheral_vascular_disease", False)
    cva = input_parameters.get("cva", False)
    tia = input_parameters.get("tia", False)
    dementia = input_parameters.get("dementia", False)
    copd = input_parameters.get("copd", False)
    connective_tissue_disease = input_parameters.get("connective_tissue_disease", False)
    peptic_ucler_disease = input_parameters.get("peptic_ucler_disease", False)
    liver_diseae = input_parameters.get("liver_disease", "none")
    diabetes_mellitus = input_parameters.get("diabetes_mellitus", "none or diet-controlled")
    hemiplegia = input_parameters.get('hemiplegia', False)
    moderate_severe_ckd = input_parameters.get("moderate_to_severe_ckd", False)
    solid_tumor = input_parameters.get("solid_tumor", "none")
    leukemia = input_parameters.get("leukemia", False )  
    lymphoma = input_parameters.get("lymphoma", False) 
    aids = input_parameters.get("aids", False)

    cci = 0

    if 49 < age < 60:
        cci += 1
    elif 59 < age < 70:
        cci += 2
    elif 69 < age < 80:
        cci += 3
    elif age >= 80:
        cci += 4

    if mi:
        cci += 1
    
    if chf:
        cci += 1
    
    if peripheral_vascular_disease:
        cci += 1
    
    if cva or tia:
        cci += 1

    if dementia:
        cci += 1
    
    if copd:
        cci += 1

    if connective_tissue_disease:
        cci += 1
    
    if peptic_ucler_disease:
        cci += 1
  
    if liver_diseae == "mild":
        cci += 1
    elif liver_diseae == "moderate to severe":
        cci += 3

    if diabetes_mellitus == "uncomplicated":
        cci += 1
    elif diabetes_mellitus == "end-organ damage":
        cci += 2

    if hemiplegia:
        cci += 2
    
    if moderate_severe_ckd:
        cci += 2
    
    if solid_tumor == "localized":
        cci += 2
    elif solid_tumor == "metastatic":
        cci += 6

    if leukemia:
        cci += 2
    
    if lymphoma:
        cci += 2

    if aids:
        cci += 6

    return cci 


def compute_cci_explanation(input_parameters):
    parameter_to_name = {"mi": "Myocardial infarction", 'chf': "Congestive heart failure", 
                         "peripheral_vascular_disease": "Peripheral vascular disease", 
                         "cva": "Cerebrovascular accident", "tia": "Transient ischemic attacks", 'connective_tissue_disease': "Connective tissue diease",
                         "dementia": "Dementia", "copd": "Chronic obstructive pulmonary disease", 'hemiplegia': "Hemiplegia",
                         "peptic_ucler_disease": "Peptic ulcer disease", "liver_disease": "Liver disease",
                         "diabetes_mellitus": "Diabetes mellitus", "moderate_to_severe_ckd": 'Moderate to severe chronic kidney disease', 
                         "solid_tumor": "Solid tumor", "leukemia": "Leukemia", "lymphoma": "Lymphoma", "aids": "AIDS",
                         "liver_disease": "Liver Disease"}
    
    
     
    two_point_params = set(['hemiplegia', "moderate_to_severe_ckd", "leukemia", "lymphoma"])
 
    age_exp, age = age_conversion.age_conversion_explanation(input_parameters["age"])
    explanation = "The current CCI is value is 0.\n"
    explanation += age_exp
    cci = 0

    if age < 50:
        explanation += f"Because the patient's age is less than 50, we do not add any points to the score, keeping the current total at {cci}.\n"
    elif 49 < age < 60:
        explanation += f"Because the patient's age is between 50 and 59, we add 1 point to the score, making the current total = {cci} + 1 = {cci + 1}.\n"
        cci += 1
    elif 59 < age < 70:
        explanation += f"Because the patient's age is between 60 and 69, we add 2 points to the score, making the current total = {cci} + 2 = {cci + 2}.\n"
        cci += 2
    elif 69 < age < 80:
        explanation += f"Because the patient's age is between 70 and 79, we add 3 points to the score, making the current total = {cci} + 3 = {cci + 3}.\n"
        cci += 3
    elif age >= 80:
        explanation += f"Because the patient's age is greater than or equal to 80 years, we add 4 points to the score, making the current total = {cci} + 4 = {cci + 4}.\n"
        cci += 4

    for parameter in parameter_to_name:

        if parameter == "tia":
            continue

        if parameter == "cva":
            explanation += "At least one of transient ischemic attack or cerebral vascular accident must be present in the patient for a point to be added to the current total.\n"

            if 'tia' not in input_parameters:
                explanation += f"Transient ischemic attacks is not reported for the patient and so we assume it to be absent.\n"
                input_parameters["tia"] = False
            elif input_parameters['tia']:
                explanation += f"Transient ischemic attacks is reported to be present for the patient.\n"
            else:
                explanation += f"Transient ischemic attacks is reported to be absent for the patient.\n"

            if 'cva' not in input_parameters:
                explanation += f"Cerebral vascular accident is not reported for the patient and so we assume it to be absent.\n"
                input_parameters["cva"] = False 
            elif input_parameters['cva']:
                explanation += f"Cerebral vascular accident is reported to be present for the patient.\n"
            else:
                explanation += f"Cerebral vascular accident is reported to be absent for the patient.\n"
           

            if input_parameters['cva'] or input_parameters['tia']:
                explanation += f"Because at least one of the issues is reported to be present for the patient, we add 1 point to the score, making the current total {cci} + 1 = {cci + 1}.\n"
                cci += 1
                continue
            else:
                explanation += f"Neither of the issues are reported to be present for the patient and so we add 0 point to the score, keeping the current total at {cci}.\n"
                continue

        if parameter == 'solid_tumor' and parameter not in input_parameters:
            explanation += f"The patient's solid tumor status is not reported and so we assume that it is 'none.' Hence, do not add any points to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'solid_tumor' and parameter in input_parameters and input_parameters[parameter] == 'none':
            explanation += f"The patient's solid tumor is reported to be 'none' and so we do not add any points to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'solid_tumor' and parameter in input_parameters and input_parameters[parameter] == 'localized':
            explanation += f"The patient's solid tumor is reported to be 'localized' and so we add 2 points to the score, making the current total {cci} + 2 = {cci + 2}.\n"
            cci += 2
            continue
        elif parameter =='solid_tumor' and parameter in input_parameters and input_parameters[parameter] == 'metastatic':
            explanation += f"The patient's solid tumor is reported to be 'metastatic' and so we add 6 points to the score, making the current total {cci} + 6 = {cci + 6}.\n"
            cci += 6
            continue

        if parameter == 'liver_diease' and parameter not in input_parameters:
            explanation +=  f"The patient's liver disease status is not reported and so we assume the value to be 'none or diet-controlled.' No points are added to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'liver_disease' and parameter in input_parameters and input_parameters[parameter] == 'none':
            explanation += f"The patient's liver disease is reported to be 'none' and so we do not add any points to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'liver_disease' and parameter in input_parameters and input_parameters[parameter] == 'mild':
            explanation += f"The patient's liver disease is reported to be 'mild' and so we add 1 point to the score, making the current total {cci} + 1 = {cci + 1}.\n"
            cci += 1
            continue
        elif parameter == 'liver_disease' and parameter in input_parameters and input_parameters[parameter] == 'moderate to severe':
            explanation += f"The patient's liver disease is reported to be 'moderate to severe' and so we add 3 points to the score, making the current total {cci} + 3 = {cci + 3}.\n"
            cci += 3
            continue

        if parameter == 'diabetes_mellitus' and 'diabetes_mellitus' not in input_parameters:
            explanation +=  f"The patient's diabetes mellitus status is not reported and so we assume the value to be 'none or diet-controlled.' No points are added to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'diabetes_mellitus' and parameter in input_parameters and input_parameters[parameter] == 'none or diet-controlled':
            explanation +=  f"The patient's diabetes mellitus is reported to be 'none or diet-controlled' and so we add 0 point to the score, keeping the current total at {cci}.\n"
            continue
        elif parameter == 'diabetes_mellitus' and parameter in input_parameters and input_parameters[parameter] == 'uncomplicated':
            explanation += f"The patient's diabetes mellitus is reported to be 'uncomplicated' and so we add 1 point to the score, making the current total {cci} + 1 = {cci + 1}.\n"
            cci += 1
            continue
        elif parameter == 'diabetes_mellitus' and parameter in input_parameters and input_parameters[parameter] == 'end-organ damage':
            explanation += f"The patient's diabetes mellitus is reported to be 'end-organ damage' and so we add 2 points to the score, making the current total {cci} + 2 = {cci + 2}.\n"
            cci += 2    
            continue


        if parameter in two_point_params and parameter in input_parameters and input_parameters[parameter]:
            explanation += f"The issue, '{parameter_to_name[parameter]},' is reported to be present for the patient and so we add 2 points to the score, making the current total {cci} + 2 = {cci + 2}.\n"
            cci += 2
        elif parameter == 'aids' and parameter in input_parameters and input_parameters['aids']:
            explanation += f'AIDS is reported to be present for the patient and so we add 6 points to the score, making the current total at {cci} + 6 = {cci + 6}.\n' 
            cci += 6

        elif parameter not in two_point_params and parameter != 'aids' and parameter in input_parameters and input_parameters[parameter]:
            explanation += f" The issue,'{parameter_to_name[parameter]},' is present for the patient and so we add 1 point to the score, making the current total {cci} + 1 = {cci + 1}.\n"
            cci += 1
        elif parameter in input_parameters and not input_parameters[parameter]:
            explanation += f"The issue, '{parameter_to_name[parameter]},' is reported to be absent for the patient and so we do not add any points to the score, keeping the current total at {cci}.\n"
        elif parameter not in input_parameters:
            explanation += f"The issue, '{parameter_to_name[parameter]},' is reported to be absent for the patient and so we do not add any points to the score, keeping the current total at {cci}.\n"

        explanation += f"The patient's CCI score is {cci} points.\n"

    return {"Explanation": explanation, "Answer": cci, "Calculator Answer": compute_cci(input_parameters)}
    


test_outputs = [
    
                {"age": [52, "years"], "mi": True, 'chf': True, 'peripheral_vascular_disease': True, 'hemiplegia': True,
                 'cva': True, 'tia': True, 'dementia': True, 'copd': True, 'connective_tissue_disease': True,
                 'peptic_ucler_disease': True, 'liver_disease': 'none', 'diabetes_mellitus': 'none or diet-controlled', 'moderate_to_severe_ckd': True, 
                 'solid_tumor': 'none', 'leukemia': True, 'lymphoma': True, 'aids': True},

                
                 {"age": [80, "years"], "mi": False, 'chf': False, 'peripheral_vascular_disease': False, 'hemiplegia': False,
                 'cva': False, 'tia': False, 'dementia': False, 'copd': False, 'connective_tissue_disease': False,
                 'peptic_ucler_disease': False, 'liver_disease': 'mild', 'diabetes_mellitus': 'uncomplicated', 'moderate_to_severe_ckd': False, 
                 'solid_tumor': 'localized', 'leukemia': False, 'lymphoma': False, 'aids': False},

                {"age": [49, "years"]}
                
                
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_cci_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/cci.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/cci.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)


'''
if parameter not in input_parameters:
            explanation += f"The issue '{parameter_to_name[parameter]}' is not reported for the patient and so we assume that it is absent for the patient. From this, we add 0 points to the score, keeping it at {cci}.\n"
            continue

'''