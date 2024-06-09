import os
import json
import unit_converter_new
import convert_temperature
import age_conversion
import mean_arterial_pressure


def compute_apache_ii_score(input_parameters):
    
    sodium = unit_converter_new.conversions(input_parameters['sodium'][0], input_parameters['sodium'][1], "mmol/L", 22.99, 1)
    pH = input_parameters['pH']
    heart_rate = input_parameters['heart_rate'][0]
    respiratory_rate = input_parameters['respiratory_rate'][0]
    potassium = unit_converter_new.conversions(input_parameters['potassium'][0], input_parameters['potassium'][1], "mmol/L", 22.99, 1)
    creatinine = unit_converter_new.conversions(input_parameters['creatinine'][0], input_parameters['creatinine'][1], "mg/dL", 113.12 , None)
    temperature = convert_temperature.fahrenheit_to_celsius(input_parameters['temperature'][0], input_parameters['temperature'][1])
    age = age_conversion.age_conversion(input_parameters['age'])
    history_of_immunocompromise = input_parameters.get('organ_failure_immunocompromise', False)
    acute_renal_failure = input_parameters.get('acute_renal_failure', False)
    chronic_renal_failure = input_parameters.get('chronic_renal_failure', False)
    hemocratit =  input_parameters['hemocratit'][0]
    wbc = unit_converter_new.convert_to_units_per_liter(input_parameters['wbc'][0], input_parameters['wbc'][1],"mm^3") 
    fio2 = input_parameters['fio2'][0]
    gcs = input_parameters['gcs']
    a_a_gradient = input_parameters.get('a_a_gradient', False)
    partial_pressure_oxygen = input_parameters.get('partial_pressure_oxygen', False)
    

    score = 0

    if history_of_immunocompromise:
        surgery_type = input_parameters.get('surgery_type', None)
        if surgery_type == 'Elective':
            score += 2 
        elif surgery_type == "Emergency":
            score += 5

    if 45 <= age <= 54:
        score += 2
    elif 55 <= age <= 64:
        score += 3
    elif 65 <= age <= 74:
        score += 5
    elif age > 74:
        score += 6

    if fio2 >= 50:
       
        if a_a_gradient > 499:
            score += 4
        elif 350 <= a_a_gradient <= 499:
            score += 3
        elif 200 <= a_a_gradient <= 349:
            score += 2
        elif a_a_gradient < 200:
            score += 0
    else:
        partial_pressure_oxygen = partial_pressure_oxygen[0]
        if partial_pressure_oxygen > 70:
            score += 0
        elif 61 <= partial_pressure_oxygen <= 70:
            score += 1
        elif 55 <= partial_pressure_oxygen <= 60:
            score += 3
        elif partial_pressure_oxygen < 55:
            score += 4

    if temperature >= 41:
        score += 4
    elif 39 <= temperature < 41:
        score += 3
    elif 38.5 <= temperature < 39:
        score += 1
    elif 34 <= temperature < 36:
        score += 1
    elif 32 <= temperature < 34:
        score += 2
    elif 30 <= temperature < 32:
        score += 3
    elif temperature < 30:
        score += 4

    map = mean_arterial_pressure.calculate_map(input_parameters)

    if map > 159:
        score += 4
    elif 129 < map <= 159:
        score += 3
    elif 109 < map <= 129:
        score += 2
    elif 69 < map <= 109:
        score += 0  # This line is technically not needed as it doesn't change the score
    elif 49 < map <= 69:
        score += 2
    elif map <= 49:
        score += 4


    if heart_rate >= 180:
        score += 4
    elif 140 <= heart_rate < 180:
        score += 3
    elif 110 <= heart_rate < 140:
        score += 2
    elif 70 <= heart_rate < 110:
        score += 0 
    elif 55 <= heart_rate < 70:
        score += 2
    elif 40 <= heart_rate < 55:
        score += 3
    elif heart_rate < 40:
        score += 4

    if respiratory_rate >= 50:
        score += 4
    elif 35 <= respiratory_rate < 50:
        score += 3
    elif 25 <= respiratory_rate < 35:
        score += 1
    elif 12 <= respiratory_rate < 25:
        score += 0  
    elif 10 <= respiratory_rate < 12:
        score += 1
    elif 6 <= respiratory_rate < 10:
        score += 2
    elif respiratory_rate < 6:
        score += 4


    if hemocratit >= 60:
        score += 4
    elif 50 <= hemocratit < 60:
        score += 2
    elif 46 <= hemocratit < 50:
        score += 1
    elif 30 <= hemocratit < 46:
        score += 0 
    elif 20 <= hemocratit < 30:
        score += 2
    elif hemocratit < 20:
        score += 4


    if wbc >= 40:
        score += 4
    elif 20 <= wbc < 40:
        score += 2
    elif 15 <= wbc < 20:
        score += 1
    elif 3 <= wbc < 15:
        score += 0 
    elif 1 <= wbc < 3:
        score += 2
    elif wbc < 1:
        score += 4


    if pH >= 7.70:
        score += 4
    elif 7.60 <= pH < 7.70:
        score += 3
    elif 7.50 <= pH < 7.60:
        score += 1
    elif 7.33 <= pH < 7.50:
        score += 0 
    elif 7.25 <= pH < 7.33:
        score += 2
    elif 7.15 <= pH < 7.25:
        score += 3
    elif pH < 7.15:
        score += 4

    if sodium >= 180:
        score += 4
    elif 160 <= sodium < 180:
        score += 3
    elif 155 <= sodium < 160:
        score += 2
    elif 150 <= sodium < 155:
        score += 1
    elif 130 <= sodium < 150:
        score += 0  
    elif 120 <= sodium < 130:
        score += 2
    elif 111 <= sodium < 120:
        score += 3
    elif sodium < 111:
        score += 4

    if potassium >= 7.0:
        score += 4
    elif 6.0 <= potassium < 7.0:
        score += 3
    elif 5.5 <= potassium < 6.0:
        score += 1
    elif 3.5 <= potassium < 5.5:
        score += 0 
    elif 3.0 <= potassium < 3.5:
        score += 1
    elif 2.5 <= potassium < 3.0:
        score += 2
    elif potassium < 2.5:
        score += 4

    if creatinine >= 3.5 and acute_renal_failure:
        score += 8
    elif 2.0 <= creatinine < 3.5 and acute_renal_failure:
        score += 6
    elif creatinine >= 3.5 and chronic_renal_failure:
        score += 4
    elif 1.5 <= creatinine < 2.0 and acute_renal_failure:
        score += 4
    elif 2.0 <= creatinine < 3.5 and chronic_renal_failure:
        score += 3
    elif 1.5 <= creatinine < 2.0 and chronic_renal_failure:
        score += 2
    elif 0.6 <= creatinine < 1.5:
        score += 0  
    elif creatinine < 0.6:
        score += 2

    score += gcs 

    return score 
    
    
def apache_ii_explanation(input_parameters):
    explanation = "The patient's current APACHE II score is 0 points.\n"
    score = 0


    sodium = unit_converter_new.conversions(input_parameters['sodium'][0], input_parameters['sodium'][1], "mmol/L", 22.99, 1)
    pH = input_parameters['pH']
    heart_rate = input_parameters['heart_rate'][0]
    respiratory_rate = input_parameters['respiratory_rate'][0]
    potassium = unit_converter_new.conversions(input_parameters['potassium'][0], input_parameters['potassium'][1], "mmol/L", 22.99, 1)
    creatinine = unit_converter_new.conversions(input_parameters['creatinine'][0], input_parameters['creatinine'][1], "mg/dL", 113.12 , None)
    age = age_conversion.age_conversion(input_parameters['age'])
    acute_renal_failure = input_parameters.get('acute_renal_failure', False)
    chronic_renal_failure = input_parameters.get('chronic_renal_failure', False)
    hemocratit =  input_parameters['hemocratit'][0]
    wbc = unit_converter_new.convert_to_units_per_liter(input_parameters['wbc'][0], input_parameters['wbc'][1],"mm^3") 
    fio2 = input_parameters['fio2'][0]
    gcs = input_parameters['gcs']
    a_a_gradient = input_parameters.get('a_a_gradient', False)
    partial_pressure_oxygen = input_parameters.get('partial_pressure_oxygen', False)

    age_explanation, age = age_conversion.age_conversion_explanation(input_parameters['age'])

    explanation += f"{age_explanation}"

    if 'organ_failure_immunocompromise' in input_parameters:
        if input_parameters['organ_failure_immunocompromise']:

            surgery_type = input_parameters.get('surgery_type', None)

            explanation += f"The patient is reported to have an organ failure of immunocompromise with a surgery type being classified as {surgery_type}. "

            if surgery_type == "Nonelective":
                explanation += f"The patient's surgery type is classified as 'Nonelective' and so 0 points are added to the total, keeping the total at 0 points.\n"
            elif surgery_type == "Elective":
                explanation += f"The patient's surgery type is classified as 'Elective' and so 2 points are added to the total, making the current total 0 + 2 = 2.\n"
                score += 2
            elif surgery_type == "Emergency":
                explanation += f"The patient's surgery type is classified as 'Emergency' and so 5 points are added to the total, making the current total 0 + 2 = 5.\n"
                score += 5
        elif not input_parameters['organ_failure_immunocompromise']:
            explanation += f"The patient is reported to not have any organ failure immunocompromise and so 0 points are added to the total, keeping the total at 0 points.\n"
    else:
        explanation += f"The patient note does not report any history on immunocompromise and so we assume this to be false. Hence, 0 points are added to the total, keeping the total at 0 points.\n"
    
    if age < 45:
        explanation += "Because the patient's age is less than 45, no points are added to the score, keeping it at 0."
    elif 45 < age <= 54:
        explanation += f"Because the patient's age is between 45 and 54, 2 points are added to the total, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 55 <= age <= 64:
        explanation += f"Because the patient's age is between 55 and 64, 3 points are added to the total, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 65 <= age <= 74:
        explanation += f"Because the patient's age is between 65 and 74, 5 points are added to the total, making the current total, {score} + 5 = {score + 5}.\n"
        score += 5
    elif age > 75:
        explanation += f"Because the patient's age is greater than 75 years, 6 points are added to the total, making the current total, {score} + 6 = {score + 6}.\n"
        score += 6

    explanation += f"The patient's FiO2 percentage is {fio2} %. "

    if fio2 >= 50:
        explanation += "Because the patent's FiO2 percentrage is greater than 50%, we need to examine the A-a-gradient to compute the APACHE II score. "
        a_a_gradient = input_parameters['a_a_gradient']
        explanation += f"The patient's A-a-gradient is {a_a_gradient}. "
        if a_a_gradient > 499:
            explanation += f"Because the patient's A-a gradient is greater than 499, we add 4 points to the total, making the current total {score + 4}.\n"
            score += 4
        elif 350 <= a_a_gradient <= 499:
            explanation += f"Because the patient's A-a gradient is between 350 and 500, we add 3 points to the total, making the current total {score + 3}.\n"
            score += 3
        elif 200 <= a_a_gradient <= 349:
            explanation += f"Because the patient's A-a gradient is between 200 and 349, we add 2 points to the total, making the current total {score + 2}.\n"
            score += 2
        elif a_a_gradient < 200:
            explanation += f"Because the patient's A-a gradient is less than 200, we do not add any points to the total, keeing the current total at {score}.\n"
            score += 0  # This line is technically not needed
    else:
        partial_pressure_oxygen = input_parameters['partial_pressure_oxygen'][0]
        explanation += "Because the patent's FiO2 percentrage is less than 50%, we need to examine the patient's A-a-gradient to compute the APACHE II score. "
        explanation += f"The patient's partial pressure of oxygen is {partial_pressure_oxygen} mm Hg. "
        if partial_pressure_oxygen > 70:
            explanation += f"Because the patient's partial pressure of oxygen is more than 70 mm Hg, we do not add any points to the total, keeing the current total at {score}.\n"
            score += 0
        elif 61 <= partial_pressure_oxygen <= 70:
            explanation += f"Because the patient's partial pressure of oxygen is between 61 and 70 mm Hg, we do add one point to the total, making the current total {score} + 1 {score + 1}.\n"
            score += 1
        elif 55 <= partial_pressure_oxygen <= 60:
            explanation += f"Because the patient's partial pressure of oxygen is between 61 and 70 mm Hg, we do add one point to the total, making the current total {score} + 1 {score + 1}.\n"
            explanation += f"Because the patient's partial pressure of oxygen is between 55 and 60 mm Hg, we add three points to the total, making the current total {score} + 3 = {score + 3}.\n"
            score += 3
        elif partial_pressure_oxygen < 55:
            explanation += f"Because the patient's partial pressure of oxygen is less than 55 mm Hg, we do add four points to the total, making the current total {score} + 4 = {score + 4}.\n"
            score += 4

    temperature_explanation, temperature = convert_temperature.fahrenheit_to_celsius_explanation(input_parameters["temperature"][0], input_parameters["temperature"][1])

    explanation += temperature_explanation + "\n"

    if temperature >= 41:
        explanation += f"Because the patient's temperature is {temperature} degrees Celsius or higher, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 39 <= temperature < 41:
        explanation += f"Because the patient's temperature is between 39 and 41 degrees Celsius, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 38.5 <= temperature < 39:
        explanation += f"Because the patient's temperature is between 38.5 and 39 degrees Celsius, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 34 <= temperature < 36:
        explanation += f"Because the patient's temperature is between 34 and 36 degrees Celsius, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 32 <= temperature < 34:
        explanation += f"Because the patient's temperature is between 32 and 34 degrees Celsius, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 30 <= temperature < 32:
        explanation += f"Because the patient's temperature is between 30 and 32 degrees Celsius, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif temperature < 30:
        explanation += f"Because the patient's temperature is below 30 degrees Celsius, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    else:
        explanation += f"The patient's temperature is within the normal range, so no additional points are added to the score, keeping the total at {score}.\n"

    map_exp = mean_arterial_pressure.mean_arterial_pressure_explanation(input_parameters)

    explanation += map_exp["Explanation"]

    map_value = map_exp["Answer"]
    
    # Mean Arterial Pressure (MAP)
    if map_value > 159:
        explanation += f"Because the patient's Mean Arterial Pressure is above 159 mmHg, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 129 < map_value <= 159:
        explanation += f"Because the patient's Mean Arterial Pressure is between 130 and 159 mmHg, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 109 < map_value <= 129:
        explanation += f"Because the patient's Mean Arterial Pressure is between 110 and 129 mmHg, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 70 <= map_value <= 109:
        explanation += f"Because the patient's Mean Arterial Pressure is between 70 and 109 mmHg, 0 points are added to the patient's score, keeping the total at {score}.\n"

    # Heart Rate
    if heart_rate >= 180:
        explanation += f"Because the patient's heart rate is 180 beats per minute or more, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 140 <= heart_rate < 180:
        explanation += f"Because the patient's heart rate is between 140 and 179 beats per minute, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 110 <= heart_rate < 140:
        explanation += f"Because the patient's heart rate is between 110 and 139 beats per minute, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 70 <= heart_rate < 110:
        explanation += f"Because the patient's heart rate is between 70 and 109 beats per minute, 0 points are added to the patient's score, keeping the total at {score}.\n"

    # Respiratory Rate
    if respiratory_rate >= 50:
        explanation += f"Because the patient's respiratory rate is 50 breaths per minute or more, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 35 <= respiratory_rate < 50:
        explanation += f"Because the patient's respiratory rate is between 35 and 49 breaths per minute, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 25 <= respiratory_rate < 35:
        explanation += f"Because the patient's respiratory rate is between 25 and 34 breaths per minute, 1 points is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 12 <= respiratory_rate < 25:
        explanation += f"Because the patient's respiratory rate is between 12 and 24 breaths per minute, 0 points are added to the patient's score, keeping the total at {score}.\n"

    # pH Levels
    if pH >= 7.70:
        explanation += f"Because the patient's pH is above 7.70, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 7.60 <= pH < 7.70:
        explanation += f"Because the patient's pH is between 7.60 and 7.69, 3 points are added to the score, making the current total {score} + 3 = {score + 4}.\n"
        score += 3
    elif 7.50 <= pH < 7.60:
        explanation += f"Because the patient's pH is between 7.50 and 7.59, 1 point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 7.33 <= pH < 7.50:
        explanation += f"Because the patient's pH is between 7.33 and 7.49, 0 points are added to the patient's score, keeping the total at {score}. "

    # Sodium Levels
    if sodium >= 180:
        explanation += f"Because the patient's sodium level is above 180 mmol/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 160 <= sodium < 180:
        explanation += f"Because the patient's sodium level is between 160 and 179 mmol/L, 3 points are added to the score, making the current total {score} + 3 = {score + 3}.\n"
        score += 3
    elif 155 <= sodium < 160:
        explanation += f"Because the patient's sodium level is between 155 and 159 mmol/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 150 <= sodium < 155:
        explanation += f"Because the patient's sodium level is between 150 and 154 mmol/L, 1 point is added to the total, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 130 <= sodium < 150:
        explanation += f"Because the patient's sodium level is between 130 and 149 mmol/L, 0 points are added to the patient's score, keeping the total at {score}. "

    # Potassium Levels
    if potassium >= 7.0:
        explanation += f"Because the patient's potassium level is above 7.0 mmol/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 6.0 <= potassium < 7.0:
        explanation += f"Because the patient's potassium level is between 6.0 and 6.9 mmol/L, 3 points are added to the score, making the current total {score} + 3 = {score + 3}.\n"
        score += 3
    elif 5.5 <= potassium < 6.0:
        explanation += f"Because the patient's potassium level is between 5.5 and 5.9 mmol/L, 1 point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 3.5 <= potassium < 5.5:
        explanation += f"Because the patient's potassium level is between 3.5 and 5.4 mmol/L, 0 points are added to the patient's score, keeping the total at {score}. "

    # Creatinine Levels
    if creatinine >= 3.5 and acute_renal_failure:
        additional_points = 8
        explanation += f"Because the patient has acute renal failure and a creatinine level above 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and acute_renal_failure:
        additional_points = 6
        explanation += f"Because the patient has acute renal failure and a creatinine level between 2.0 and 3.4, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif creatinine >= 3.5 and chronic_renal_failure:
        additional_points = 4
        explanation += f"Because the patient has chronic renal failure and a creatinine level above 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and chronic_renal_failure:
        additional_points = 3
        explanation += f"Because the patient has chronic renal failure and a creatinine level between 2.0 and 3.4, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and acute_renal_failure:
        additional_points = 4
        explanation += f"Because the patient has acute renal failure and a creatinine level between 1.5 and 1.9, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and chronic_renal_failure:
        additional_points = 2
        explanation += f"Because the patient has chronic renal failure and a creatinine level between 1.5 and 1.9, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 0.6 <= creatinine < 1.5:
        explanation += f"Because the patient's creatinine level is between 0.6 and 1.4, no points are added to the score, keeping the current total at {score}.\n"
    elif creatinine < 0.6:
        additional_points = 2
        explanation += f"Because the patient's creatinine level is below 0.6, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points

    # Hematocrit Levels
    if hemocratit >= 60:
        explanation += f"Because the patient's hemocratit is 60% or higher, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 50 <= hemocratit < 60:
        explanation += f"Because the patient's hemocratit is between 50% and 59%, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 46 <= hemocratit < 50:
        explanation += f"Because the patient's hemocratit is between 46% and 49%, 1 points is added to the score, making the current total {score} + 1= {score + 1}.\n"
        score += 1
    elif 30 <= hemocratit < 46:
        explanation += f"Because the patient's hemocratit is between 30% and 45%, 0 points are added to the patient's score, keeping the total at {score}. "

    # WBC Count
    if wbc >= 40:
        explanation += f"Because the patient's white blood cell count is above 40 x10^9/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 20 <= wbc < 40:
        explanation += f"Because the patient's white blood cell count is between 20 and 39.9 x10^9/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 15 <= wbc < 20:
        explanation += f"Because the patient's white blood cell count is between 15 and 19.9 x10^9/L, 1 points is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 3 <= wbc < 15:
        explanation += f"Because the patient's white blood cell count is between 3 and 14.9 x10^9/L, 0 points are added to the patient's score, keeping the total at {score}. "

    explanation += f"The patient's Glasgow Coma Score is {gcs}, and so we add {gcs} points to the total making the current total {gcs} + {score} = {gcs + score}. Hence, the patient's APACHE II score is {gcs + score}.\n"
    score += gcs

    return {"Explanation": explanation, "Answer": score, "Calculator Answer": compute_apache_ii_score(input_parameters)}