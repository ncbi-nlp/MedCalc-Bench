import os
import json 
import unit_converter_new

def compute_child_pugh_score(input_variables):
 
    inr = input_variables['inr']

    ascites_state = input_variables.get('ascites', 'Absent')
    encephalopahty_state = input_variables.get('encephalopathy', 'No Encephalopathy')

    bilirubin = unit_converter_new.conversions(input_variables['bilirubin'][0], input_variables['bilirubin'][1], "mg/dL", 584.66, None)
    albumin = unit_converter_new.conversions(input_variables['albumin'][0], input_variables['albumin'][1], "g/dL", 66500, None)

    bilirubin_score = 0
    albumin_score = 0
    inr_score = 0
    ascites_score = 0
    enc_score = 0
    
    if bilirubin < 2: 
        bilirubin_score += 1
    elif 2 < bilirubin < 3:
        bilirubin_score += 2
    elif bilirubin > 3:
        bilirubin_score += 3

    if albumin > 3.5: 
        albumin_score += 1
    elif 2.8 < albumin < 3.5:
        albumin_score += 2
    elif albumin < 2.8:
        albumin_score += 3

    if inr < 1.7: 
        inr_score += 1
    elif 1.7 <= inr <= 2.3:
        inr_score += 2
    elif inr > 2.3:
        inr_score += 3

    if ascites_state == 'Absent':
        ascites_score += 1 
    elif ascites_state == 'Slight':
        ascites_score += 2
    elif ascites_state == 'Moderate':
        ascites_score += 3
    

    if encephalopahty_state == 'No Encephalopathy':
        enc_score += 1 
    elif encephalopahty_state == 'Grade 1-2':
        enc_score += 2
    elif encephalopahty_state== 'Grade 3-4':
        enc_score += 3

    return bilirubin_score + albumin_score + inr_score + ascites_score + enc_score


def compute_child_pugh_score_explanation(input_variables):

    cp_score = 0

    explanation = "The current child pugh score is 0.\n"

    inr = input_variables['inr']

    ascites_state = input_variables.get('ascites', 'Absent')
    encephalopathy_state = input_variables.get('encephalopathy', 'No Encephalopathy')

    explanation += f"The patient's INR is {inr}. "
    bilirubin_exp, bilirubin = unit_converter_new.conversion_explanation(input_variables['bilirubin'][0], 'bilirubin', 548.66, None, input_variables['bilirubin'][1], "mg/dL")
    albumin_exp, albumin = unit_converter_new.conversion_explanation(input_variables['albumin'][0], 'albumin', 66500, None, input_variables['albumin'][1], "g/dL")


    # INR score calculation
    if inr < 1.7: 
        explanation += f"Because the INR is less than 1.7, we add 1 to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
        cp_score += 1
    elif 1.7 <= inr <= 2.3:
        explanation += f"Because the INR is between 1.7 and 2.3, we add two to the score, making the current total {cp_score} + 2 = {cp_score + 2}.\n"
        cp_score += 2
    elif inr > 2.3:
        explanation +=  f"Because the INR is greater than 2.3, we add three to the score, making the current total {cp_score} + 3 = {cp_score + 3}.\n"
        cp_score += 3

    explanation += bilirubin_exp

    # Bilirubin score calculation
    if bilirubin < 2: 
        explanation += f"Because the Bilirubin concentration is less than 2 mg/dL, we add 1 to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
        cp_score += 1
    elif 2 < bilirubin < 3:
        explanation += f"Because the Bilirubin concentration is between 2 mg/dL and 3 mg/dL, we add 2 to the score, making the current total {cp_score} + 2 = {cp_score + 2}.\n"
        cp_score += 2
    elif bilirubin >= 3:
        explanation += f"Because the Bilirubin concentration is greater than 3 mg/dL, we add 3 to the score, making the current total {cp_score} + 3 = {cp_score + 3}.\n"
        cp_score += 3

    explanation += albumin_exp

    # Albumin score calculation
    if albumin > 3.5: 
        explanation += f"Because the Albumin concentration is greater than 3.5 g/dL, we add 1 to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
        cp_score += 1
    elif 2.8 < albumin <= 3.5:
        explanation += f"Because the Albumin concentration is between 2.8 g/dL and 3.5 g/dL, we add 2 to the score, making the current total {cp_score} + 2 = {cp_score + 2}.\n"
        cp_score += 2 
    elif albumin <= 2.8:
        explanation += f"Because the Albumin concentration is less than 2.8 g/dL, we add 3 to the score, making the current total {cp_score} + 3 = {cp_score + 3}.\n"
        cp_score += 3

    # Ascites score calculation
    if 'ascites' in input_variables:

        if input_variables['ascites'] == 'Absent':
            explanation += f"Ascites is reported to be 'absent' and so we add 1 point to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
            cp_score += 1
        elif ascites_state == 'Slight':
            explanation += f"Ascites is reported to be 'slight' and so we add 2 points to the score, making the current total {cp_score} + 2 = {cp_score + 2}.\n"
            cp_score += 2
        elif ascites_state == 'Moderate':
            explanation += f"Ascites is reported to be 'moderate' and so we add 3 points to the score, making the current total {cp_score} + 3 = {cp_score + 3}.\n"
            cp_score += 3
    else:
        explanation += f"The Ascites state not specified, assuming and so we will assume it to be absent. This means we add 1 point to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
        cp_score += 1

    if 'encephalopathy' in input_variables:
        # Encephalopathy score calculation
        if encephalopathy_state == 'No Encephalopathy':
            explanation +=  f"Encephalopathy state is reported to be 'no encephalopathy' and so we add one point to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
            cp_score += 1
        elif encephalopathy_state == 'Grade 1-2':
            explanation += f"Encephalopathy state is 'Grade 1-2 encephalopathy' and so we add two points to the score, making the current total {cp_score} + 2 = {cp_score + 2}.\n"
            cp_score += 2
        elif encephalopathy_state == 'Grade 3-4':
            explanation += f"Encephalopathy state is 'Grade 3-4 encephalopathy' and so we add three points to the score, making the current total {cp_score} + 3 = {cp_score + 3}.\n"
            cp_score += 3
    else:
        explanation += f"Encephalopathy state is not specified, and so we assume it's value to be 'no encephalopathy.' We add one point to the score, making the current total {cp_score} + 1 = {cp_score + 1}.\n"
        cp_score += 1

    explanation += f"The patient's child pugh score is {cp_score}.\n"

    return {"Explanation": explanation, "Answer": cp_score, "Calculator Answer": compute_child_pugh_score(input_variables)}


test_outputs = [{"albumin": [3.7, "g/dL"],
                 "bilirubin": [2, "mg/dL"], 
                 'inr': 2,
                 'ascites': "Slight", 
                 'encephalopathy': 'Grade 1-2'}, 

                {"albumin": [3, "g/dL"],
                 "bilirubin": [2.5, "mg/dL"], 
                 'inr': 1.5,
                 'ascites': "Absent", 
                 'encephalopathy': 'No Encephalopathy'}, 

                {"albumin": [2.5, "g/dL"],
                 "bilirubin": [1.9, "mg/dL"], 
                 'inr': 3.6,
                 'ascites': "Moderate", 
                 'encephalopathy': 'Grade 3-4'}, 
                
                {"albumin": [2.5, "g/dL"],
                 "bilirubin": [2.5, "mg/dL"], 
                 'inr': 1.0}]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_child_pugh_score_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/child_pugh.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/child_pugh.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)


    
