import os
import json 
from rounding import round_number

def rautaharju_calculator(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval_ms = input_variables["qt_interval"][0]

    qt_interval = qt_interval_ms

    qt_c = qt_interval * (120 + heart_rate) / 180

    return qt_c

def rautaharju_calculator_explanation(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval = input_variables["qt_interval"][0]

    explanation = "The corrected QT interval using the Rautajarju formula is computed as  QTc = QT interval x (120 + HR) / 180, where QT interval is in msec, and HR is the heart rate in beats per minute.\n"

    explanation += f"The QT interval is {qt_interval} msec.\n"
    explanation += f"The patient's heart rate is {heart_rate} beats per minute.\n"

    qt_c = round_number(qt_interval * (120 + heart_rate) / 180)
    
    explanation += f"Hence, plugging in these values, we will get {qt_interval} x (120 + {heart_rate}) / 180 = {qt_c}.\n"
    explanation += f"The patient's corrected QT interval (QTc) is {qt_c} msec.\n"

    return {"Explanation": explanation, "Answer": qt_c, "Calculator Answer": rautaharju_calculator(input_variables)}


test_outputs = [
    {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]},  
    {"heart_rate": [60, "beats per minute"], "qt_interval": [350, "msec"]},  
    {"heart_rate": [90, "beats per minute"], "qt_interval": [450, "msec"]}, 
]

outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = rautaharju_calculator_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/qt_calculator_rautaharju.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/qt_calculator_rautaharju.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)