import os
import json
import age_conversion

def calculate_cha2ds2_vasc_score(params):

    age = age_conversion.age_conversion(params['age'])
    sex = params['sex']
    chf = params.get('chf', False)
    hypertension = params.get('hypertension', False)
    stroke = params.get('stroke', False)
    tia = params.get('tia', False)
    thromboembolism = params.get('thromboembolism', False)
    vascular_disease = params.get('vascular_disease', False)
    diabetes = params.get('diabetes', False)
    
  
    age_score = 2 if age >= 75 else (1 if age >= 65 else 0)
    sex_score = 1 if sex.lower() == 'female' else 0
    chf_score = 1 if chf else 0
    hypertension_score = 1 if hypertension else 0
    stroke_tia_thromboembolism_score = 2 if stroke or tia or thromboembolism else 0
    vascular_disease_score = 1 if vascular_disease else 0
    diabetes_score = 1 if diabetes else 0
    
    total_score = age_score + sex_score + chf_score + hypertension_score + stroke_tia_thromboembolism_score + vascular_disease_score + diabetes_score
    
    return total_score


def generate_cha2ds2_vasc_explanation(params):

    score = 0
   
    output = "The current CHA2DS2-VASc score is 0.\n"

    text, age = age_conversion.age_conversion_explanation(params['age'])
    output += text

      # Age
    if age >= 75:
        output += f"Because the age is greater than 74, two points added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif age >= 65:
        output += f"Because the age is between 65 and 74, one point added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    else:
        output += f"Because the age is less than 65 years, no points are added to the current total, keeping the total at {score}.\n"

    sex = params['sex']  # Sex of the patient (Male/Female)

    output += f"The patient's gender is {sex.lower()} "

    if sex.lower() == 'female':
        output += f"and so one point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    else:
        output += f"and so no points are added to the current total, keeping the total at {score}.\n"

    # Congestive Heart Failure
    if 'chf' in params:
        chf = params['chf']
        output += f"The patient history for congestive heart failure is {'present' if chf else 'absent'}. "
    else:
        chf = False
        output += f"Because the congestive heart failure history is not specified in the patient note, we assume it is absent from the patient. "

    # Congestive Heart Failure (CHF)
    if chf:
        output += f"Because the patient has congestive heart failure, one point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    else:
        output += f"Because the patient does not have congestive heart failure, no points are added to the current total, keeping the total at {score}.\n"


    # Hypertension
    if 'hypertension' in params:
        hypertension = params['hypertension']
        output += f"The patient history for hypertension is {'present' if hypertension else 'absent'}. "
    else:
        hypertension = False
        output += f"Because hypertension history is not specified in the patient note, we assume that it is absent from the patient. "

     # Congestive Heart Failure (CHF)
    if hypertension:
        output += f"Because the patient has hypertension, one point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    else:
        output += f"Because the patient does not have hypertension, no points are added to the current total, keeping the total at {score}.\n"
   
    output += f"One criteria of the CHA2DS2-VASc score is to check if the patient has had any history of stroke, transient ischemic attacks (TIA), or thromboembolism. "    

    if 'stroke' in params:
        stroke = params['stroke']
        output += f"Based on the patient note, the patient history for stroke is {'present' if stroke else 'absent'}. "
    else:
        stroke = False
        output += f"Because stroke history is not specified in the patient note, we assume that it is absent from the patient. "

    if 'tia' in params:
        tia = params['tia']
        output += f"Based on the patient note, the patient history for tia is {'present' if tia else 'absent'}. "
    else:
        tia = False
        output += f"Because tia history is not specified in the patient note, we assume that it is absent from the patient. "

    if 'thromboembolism' in params:
        thromboembolism = params['thromboembolism']
        output += f"Based on the patient note, the patient history for thromboembolism is {'present' if thromboembolism else 'absent'}. "
    else:
        thromboembolism = False
        output += f"Because thromboembolism history is not specified in the patient note, we assume it to be absent. "

    # Stroke / TIA / Thromboembolism
    if stroke or tia or thromboembolism:
        output += f"Because at least one of stroke, tia, or thromboembolism is present, two points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    else:
        output += f"Because all of stroke, tia, or thromboembolism are absent, no points are added to score, keeping the score at {score}.\n"

    if 'vascular_disease' in params:
        vascular_disease = params['vascular_disease']
        output += f"Based on the patient note, the patient history for vascular disease is {'present' if vascular_disease else 'absent'}. "
    else:
        vascular_disease = False
        output += f"Because vascular disease history is not specified in the patient note, we assume it to be absent.\n"

    if vascular_disease:
        output += f"Because the patient has vascular disease, one point is added to the score, making the current total {score} + 1 = {score + 1}. "
        score += 1
    else:
        output += f"Because the patient does not have vascular disease, no points are added to score, keeping the score at {score}. "

    if 'diabetes' in params:
        diabetes = params['diabetes']
        output += f"Based on the patient note, the patient history for diabetes is {'present' if diabetes else 'absent'}. "
    else:
        diabetes = False
        output += f"Because diabetes history is not specified in the patient note, we assume it's value as 'absent'. "

    if diabetes:
        output += f"Because the patient has diabetes, one point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    else:
        output += f"Because the patient does not have diabetes, no points are added to score, keeping the score at {score}.\n"

    output += f"The patient's CHA2DS2-VASc Score is {score}.\n"

    return {"Explanation": output, "Answer": score, "Calculator Answer": calculate_cha2ds2_vasc_score(params)}



test_outputs = [{"age": [75, "years"], 
                 "sex": "Female", 
                 "chf": True,
                 "hypertension": True, 
                 "stroke": True, 
                 "tia": True, 
                 "thromboembolism": True, 
                 "vascular_disease": True, 
                 "diabetes": True}, 

                 {"age": [14, "years"], 
                 "sex": "Male", 
                 "chf": False,
                 "hypertension": False, 
                 "stroke": False, 
                 "tia": False, 
                 "thromboembolism": False, 
                 "vascular_disease": False, 
                 "diabetes": False}, 

                {"age": [14, "years"], 
                 "sex": "Male", 
                 "hypertension": False, 
                 "thromboembolism": True, 
                 "vascular_disease": False, 
                 "diabetes": False}
                 
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = generate_cha2ds2_vasc_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"


file_name = "explanations/cha2ds2_vasc_score.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)



file_name = "explanations/cha2ds2_vasc_score.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
