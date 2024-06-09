import os 
import json
import age_conversion

def compute_heart_score(input_variables):

    heart_score = 0
    history_dict = {"Slightly suspicious": 0, "Moderately suspicious": 1, "Highly suspicious": 2}
    electrocardiogram_dict = {'Normal': 0, 'Non-specific repolarization disturbance': 1, 'Significant ST deviation': 2}
    initial_troponin_dict =  {'less than or equal to normal limit': 0, 'between the normal limit or up to three times the normal limit': 1, 'greater than three times normal limit': 2}
    risk_factors = {'hypertension': 1, 'hypercholesterolemia': 1, 'diabetes_mellitus': 1,
                         'obesity': 1, 'smoking': 1, 'family_with_cvd': 1, 'atherosclerotic_disease': 1}
    
    history_value = input_variables.get("history", "Slightly suspicious")
    electrocardiogram_value = input_variables.get("electrocardiogram", "Normal")
    initial_troponin_value = input_variables.get("initial_troponin", 'less than or equal to normal limit')
    age_value = age_conversion.age_conversion(input_variables["age"])

    heart_score += history_dict[history_value]
    heart_score += electrocardiogram_dict[electrocardiogram_value]
    heart_score += initial_troponin_dict[initial_troponin_value]

    if 45 <= age_value < 65:
        heart_score += 1
    elif age_value >= 65:
        heart_score += 2

    num_risk_factors = 0

    for factor in risk_factors:
        
        factor_value = input_variables.get(factor)

        if factor_value is None:
            input_variables[factor] = False

        if input_variables[factor]:
            num_risk_factors += 1

    if 1 <= num_risk_factors <= 2:
        heart_score += 1
    elif num_risk_factors >= 3 or input_variables["atherosclerotic_disease"]:
        heart_score += 2
        
    return heart_score
            
def compute_heart_score_explanation(input_parameters):

    # Define parameters and their default values
    parameters = {
        'history': {'Slightly suspicious': 0, 'Moderately suspicious': 1, 'Highly suspicious': 2},
        'electrocardiogram': {'Normal': 0, 'Non-specific repolarization disturbance': 1, 'Significant ST deviation': 2},
        'age': {'< 45': 0, '45 - 65': 1, '> 65': 2},
        'risk_factors': {'hypertension': 1, 'hypercholesterolemia': 1, 'diabetes_mellitus': 1,
                         'obesity': 1, 'smoking': 1, 'family_with_cvd': 1, 'atherosclerotic_disease': 1},
        'initial_troponin': {'less than or equal to normal limit': 0, 'between the normal limit or up to three times the normal limit': 1, 'greater than three times normal limit': 2}
    }

    factor_name = {'hypertension': 'hypertension', 'hypercholesterolemia': 'hypercholesterolemia',  
                   'diabetes_mellitus': 'diabetes mellitus', 'obesity': 'obesity', 'smoking': 'smoking', 
                   'family_with_cvd': "family with cvd", 'atherosclerotic_disease': "atherosclerotic disease", 'initial_tropopin': 'initial tropopin'}

    default_value = {'history': 'Slightly suspicious', 'electrocardiogram': 'Normal', 'initial_troponin': 'less than or equal to normal limit'}

    # Initialize total score and output explanation
    total_score = 0
    explanation = "The current HEART Score is 0.\n"

    for param, options in parameters.items():
        param_value = input_parameters.get(param)

        if param == 'risk_factors':
           
            present_factors = [factor for factor in options.keys() if factor in input_parameters and input_parameters[factor]]
            present_factors_names = [factor_name[factor] for factor in options.keys() if factor in input_parameters and input_parameters[factor]]

            if present_factors:
                    explanation += f"The following risk factor(s) are present based on the patient's note: {', '.join(present_factors_names)}. " 

            present_but_false = [factor for factor in options.keys() if factor in input_parameters and not input_parameters[factor]]
            present_but_false_names = [factor_name[factor] for factor in options.keys() if factor in input_parameters and not input_parameters[factor]]

            if present_but_false:
                    explanation += f"The following risk factor(s) are mentioned in the patient's note, but these risk factors are noted to be absent from the patient: {', '.join(present_but_false_names)}. "
                    for item in present_but_false:
                        input_parameters[item] = False

            missing_factors = [factor for factor in options.keys() if factor not in input_parameters]
            missing_factors_names = [factor_name[factor] for factor in options.keys() if factor in input_parameters and not input_parameters[factor]]

            if missing_factors:
                explanation += f"The following risk factor(s) are missing from the patient's data: {', '.join(missing_factors_names)}. We will assume that these are all absent from the patient. "

            for factor in missing_factors:
                input_parameters[factor] = False

            factors = present_factors + missing_factors + present_but_false
              
        elif param in ['history', 'electrocardiogram', 'initial_troponin']:

            if param == 'initial_troponin':
                param_name = 'initial troponin'
            else:
                param_name = param

            if param not in input_parameters:
                explanation += f"'{param_name}' is missing from the patient's data and so we assume it's value is {default_value[param]}."
                input_parameters[param] = default_value[param]
            else:
                explanation += f"The value of '{param_name}' in the patient's note is determined to be '{param_value}'. "

        elif param == "age":
                age_explanation, age = age_conversion.age_conversion_explanation(input_parameters["age"])
                explanation += age_explanation
       
        # Add points based on parameter value
        if param == 'risk_factors':
            # Compute the number of risk factors
            risk_factors_count = sum(1 for factor in factors if input_parameters[factor])
            explanation += f"Based on the HEART Score risk factors criteria, {risk_factors_count} risk factors are present and so "

            if risk_factors_count == 0:
                explanation += f"0 points are added for the risk factors criteria, keeping the current total at {total_score}.\n"
            elif 1 <= risk_factors_count <= 2:
                explanation += f"1 point is added for the risk factors criteria, making the current total, {total_score} + 1 = {total_score + 1}.\n"
                total_score += 1
            elif risk_factors_count < 3 and input_parameters['atherosclerotic_disease']:
                explanation += f"2 points are added for the risk factors criteria as atherosclerotic disease is present, making the current total {total_score} + 2 = {total_score + 2}.\n"
                total_score += 2
            elif risk_factors_count >= 3:
                explanation += f"2 points are added as 3 or more risk factors are present, making the current total {total_score} + 2 = {total_score + 2}.\n"
                total_score += 2

        elif param == "age":
            if age < 45:
                explanation += f"The patient's age is less than 45 years and so keep the current total at {total_score}.\n"
            elif 45 <= age < 65:
                explanation += f"The patient's age is between 45 and 65 years and so we increment the current total by 1, making the current total {total_score} + 1 = {total_score + 1}.\n"
                total_score += 1
            else:
                explanation += f"The patient's age is greater than 65 years and so we increment the current total by 2, making the current total {total_score} + 2 = {total_score + 2}.\n"
                total_score += 2
        else:

            points = options[input_parameters[param]]

            if param == 'initial_troponin':
                param = 'initial troponin'

            if points == 0:
                explanation += f"Based on the HEART Score criteria, 0 points are added for '{param}', keeping the current total at {total_score}.\n"
            elif points == 1:
                explanation += f"Based on the HEART Score criteria, 1 point is added for '{param}', increasing the current total to {total_score} + 1 = {total_score + 1}.\n"
                total_score += 1
            else:
                explanation += f"Based on the HEART Score criteria, 2 points are added for '{param}', increasing the current total to {total_score} + 2 = {total_score + 2}.\n"
                total_score += 2

    explanation += f"Based on the patient's data, the HEART Score is {total_score}.\n"

    return {"Explanation": explanation, "Answer": total_score, "Calculator Answer": compute_heart_score(input_parameters)}
        

test_outputs = [
    {
        'history': 'Slightly suspicious',
        'electrocardiogram': 'Normal',
        'age': [40, 'years'],
        'hypertension': False,
        'hypercholesterolemia': False,
        'diabetes_mellitus': False,
        'obesity': False,
        'smoking': False,
        'family_with_cvd': False,
        'atherosclerotic_disease': False,
        'initial_troponin': 'less than or equal to normal limit'
    },
    {
        'history': 'Moderately suspicious',
        'electrocardiogram': 'Non-specific repolarization disturbance',
        'age': [60, 'years'],
        'hypertension': True,
        'hypercholesterolemia': False,
        'diabetes_mellitus': True,
        'obesity': False,
        'smoking': True,
        'family_with_cvd': False,
        'atherosclerotic_disease': False,
        'initial_troponin': 'between the normal limit or up to three times the normal limit'
    },
    {
        'history': 'Highly suspicious',
        'electrocardiogram': 'Significant ST deviation',
        'age': [70, 'years'],
        'hypertension': True,
        'hypercholesterolemia': True,
        'diabetes_mellitus': True,
        'obesity': True,
        'smoking': True,
        'family_with_cvd': True,
        'atherosclerotic_disease': True,
        'initial_troponin': 'greater than three times normal limit'
    },

       {
        'history': 'Highly suspicious',
        'electrocardiogram': 'Significant ST deviation',
        'age': [70, 'years'],
        'hypertension': False,
        'family_with_cvd': False,
        'initial_troponin': 'greater than three times normal limit'
    }
]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_heart_score_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/heart_score.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/heart_score.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
