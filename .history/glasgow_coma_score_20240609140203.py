import os 
import json 


def compute_glasgow_coma_score_explanation(input_variables):

    glasgow_dictionary = {"best_eye_response": {"eyes open spontaneously": 4, "eye opening to verbal command": 3, "eye opening to pain": 2, "no eye opening": 1, 'not testable': 4},
                          "best_verbal_response": {"oriented": 5, "confused": 4, "inappropriate words": 3, "incomprehensible sounds": 2, "no verbal response": 1, 'not testable': 4},
                          "best_motor_response": {"obeys commands": 6, "localizes pain": 5, "withdrawal from pain": 4, "flexion to pain": 3, "extension to pain": 2, "no motor response": 1},
                          }

    best_eye_response_value = input_variables["best_eye_response"]
    best_verbal_response_value = input_variables["best_verbal_response"]
    best_motor_response_value = input_variables["best_motor_response"]

    eye_score = glasgow_dictionary["best_eye_response"][best_eye_response_value]
    verbal_score = glasgow_dictionary["best_verbal_response"][best_verbal_response_value]
    motor_score = glasgow_dictionary["best_motor_response"][best_motor_response_value]

    glasgow_score = 0

    eye_point = "points" if eye_score == 0 or eye_score > 1 else "point"
    verbal_point = "points" if verbal_score == 0 or verbal_score > 1 else "point"
    motor_point = "points" if motor_score == 0 or motor_score > 1 else "point"

    
    explanation = "The current glasgow coma score is 0.\n" 

    if best_eye_response_value == 'not testable': 
        explanation += f"Based on the patient note, the best eye response for the patient is '{best_eye_response_value}', and so we assume the the patient can open his or her eyes spontaneously. Hence, we add {eye_score} {eye_point}, making the current total {glasgow_score} + {eye_score} = {glasgow_score + eye_score}.\n"
        glasgow_score += eye_score
    else:
        explanation += f"Based on the patient note, the best eye response for the patient is '{best_eye_response_value}', and so we add {eye_score} {eye_point} making the current total {glasgow_score} + {eye_score} = {glasgow_score + eye_score}.\n"
        glasgow_score += eye_score

    if best_verbal_response_value == 'not testable': 
        explanation += f"Based on the patient note, the best verbal response for the patient is '{best_verbal_response_value}', and so we assume the the patient's verbal response is oriented. Hence, we add {verbal_score} {verbal_point}, making the current total {glasgow_score} + {verbal_score} = {glasgow_score + verbal_score}.\n"
        glasgow_score += verbal_score
    else:
        explanation += f"Based on the patient note, the best verbal response for the patient is '{best_verbal_response_value}', and so we add {verbal_score} {verbal_point} making the current total {glasgow_score} + {verbal_score} = {glasgow_score + verbal_score}.\n"
        glasgow_score += verbal_score
   
    explanation += f"Based on the patient note, the best motor response for the patient is '{best_motor_response_value}', and so we add {motor_score} {motor_point} making the current total {glasgow_score} + {motor_score} = {glasgow_score + motor_score}.\n"
    glasgow_score += motor_score
    explanation += f"Hence, the patient's glasgow coma score is {glasgow_score}.\n"

    return {"Explanation": explanation , "Answer": glasgow_score}


test_outputs = [{"best_eye_response": "eye opening to verbal command", 
                 "best_verbal_response": "inappropriate words",
                 "best_motor_response": "localizes pain"}, 

                {"best_eye_response": "eyes open spontaneously", 
                 "best_verbal_response": "oriented",
                 "best_motor_response": "obeys commands"},

                {"best_eye_response": "no eye opening", 
                 "best_verbal_response": "no verbal response",
                 "best_motor_response": "no motor response"},
                 
                ]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = compute_glasgow_coma_score_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/gcs.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''


file_name = "explanations/gcs.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)
