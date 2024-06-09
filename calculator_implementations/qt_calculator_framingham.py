import os
import json 
from rounding import round_number


def framingham_calculator(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval_ms = input_variables["qt_interval"][0]

    qt_interval = qt_interval_ms

    rr_interval_sec = 60 / heart_rate

    qt_c = qt_interval + (154 * (1 - rr_interval_sec))

    return qt_c

def framingham_calculator_explanation(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval = input_variables["qt_interval"][0]

    explanation = "The corrected QT interval using the Framingham formula is computed as  QTc = QT Interval + (154 * (1 - rr_interval_sec)), where QT interval is in msec, and RR interval is given as 60/(heart rate).\n"

    explanation += f"The patient's heart rate is {heart_rate} beats per minute.\n"
    explanation += f"The QT interval is {qt_interval} msec.\n"

    rr_interval_sec = round_number(60 / heart_rate)
    explanation += f"The RR interval is computed as 60/(heart rate), and so the RR interval is 60/{heart_rate} = {rr_interval_sec}.\n"

    qt_c =  round_number(qt_interval + (154 * (1 - rr_interval_sec)))
    explanation += f"Hence, plugging in these values, we will get {qt_interval}/(154 * ( 1- {rr_interval_sec} )) = {qt_c}.\n"

    explanation += f"The patient's corrected QT interval (QTc) is {qt_c} msec.\n"

    return {"Explanation": explanation, "Answer": qt_c, "Calculator Answer": framingham_calculator(input_variables)}


test_outputs = [
    {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]},  
    {"heart_rate": [60, "beats per minute"], "qt_interval": [350, "msec"]},  
    {"heart_rate": [90, "beats per minute"], "qt_interval": [450, "msec"]}, 
]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = framingham_calculator_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"


'''
file_name = "explanations/qt_calculator_framingham.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/qt_calculator_framingham.txt"

with open(file_name, 'w') as file:
    file.write(explanations)