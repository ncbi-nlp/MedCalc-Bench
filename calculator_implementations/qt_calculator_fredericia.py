import os
import json 
from rounding import round_number


def fredericia_calculator(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval_ms = input_variables["qt_interval"][0]

    qt_interval_sec = qt_interval_ms

    rr_interval_sec = 60 / heart_rate

    qt_c = qt_interval_sec / (rr_interval_sec) ** (1/3)

    return qt_c

def fredericia_calculator_explanation(input_variables):
    heart_rate = input_variables["heart_rate"][0]
    qt_interval = input_variables["qt_interval"][0]

    explanation = "The corrected QT interval using the Fredericia formula is computed as  QTc = QT interval / (RR interval)**(1/3), where ** denotes an exponent, QT interval is in msec, and RR interval is given as 60/(heart rate).\n"

    explanation += f"The patient's heart rate is {heart_rate} beats per minute.\n"
    explanation += f"The QT interval is {qt_interval} msec.\n"

    rr_interval_sec = round_number(60 / heart_rate)
    explanation += f"The RR interval is computed as 60/(heart rate), and so the RR interval is 60/{heart_rate} = {rr_interval_sec}.\n"

    qt_c = round_number(qt_interval/(rr_interval_sec) ** (1/3))
    explanation += f"Hence, plugging in these values, we will get {qt_interval}/√({rr_interval_sec}) = {qt_c}."

    explanation += f"The patient's corrected QT interval (QTc) is {qt_c} msec. "

    return {"Explanation": explanation, "Answer": qt_c, "Calculator Answer": fredericia_calculator(input_variables)}



test_outputs = [
    {"heart_rate": [75, "beats per minute"], "qt_interval": [400, "msec"]},  
    {"heart_rate": [60, "beats per minute"], "qt_interval": [350, "msec"]},  
    {"heart_rate": [90, "beats per minute"], "qt_interval": [450, "msec"]}, 
]


outputs = {}
explanations = ""
for i, test_case in enumerate(test_outputs):
    outputs[i] = fredericia_calculator_explanation(test_case)
    explanations += "Explanation:\n"
    explanations += outputs[i]["Explanation"]
    explanations += "\n"

'''
file_name = "explanations/qt_calculator_fredericia.json"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    json.dump(outputs, file, indent=4)
'''

file_name = "explanations/qt_calculator_fredericia.txt"
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as file:
    file.write(explanations)