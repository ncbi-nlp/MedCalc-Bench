import unit_converter_new
import convert_temperature
import age_conversion
import mean_arterial_pressure
    
def apache_ii_explanation(input_parameters):

    
    explanation = """The criteria for the APACHE II Score are listed below:

1. Age, years: ≤44 = 0 points, 45-54 = +2 points, 55-64 = +3 points, 65-74 = +5 points, ≥75 = +6 points
2. History of severe organ insufficiency or immunocompromised: Yes, nonoperative or emergency postoperative patient = +5 points, Yes, elective postoperative patient = +2 points, No = 0 points
3. Rectal temperature, °C: ≥41 = +4 points, 39 to <41 = +3 points, 38.5 to <39 = +1 point, 36 to <38.5 = 0 points, 34 to <36 = +1 point, 32 to <34 = +2 points, 30 to <32 = +3 points, <30 = +4 points
4. Mean arterial pressure, mmHg: ≥160 = +4 points, 130-159 = +3 points, 110-129 = +2 points, 70-109 = 0 points, 50-69 = +2 points, 40-49 = +3 points, <40 = +4 points
5. Heart rate, beats per minute: ≥180 = +4 points, 140 to <180 = +3 points, 110 to <140 = +2 points, 70 to <110 = 0 points, 55 to <70 = +2 points, 40 to <55 = +3 points, <40 = +4 points
6. Respiratory rate, breaths per minute: ≥50 = +4 points, 35 to <50 = +3 points, 25 to <35 = +1 point, 12 to <25 = 0 points, 10 to <12 = +1 point, 6 to <10 = +2 points, <6 = +4 points
7. Oxygenation (use PaO₂ if FiO₂ < 50%, otherwise use A-a gradient): A-a gradient > 499 = +4 points, A-a gradient 350-499 = +3 points, A-a gradient 200-349 = +2 points, A-a gradient < 200 (if FiO₂ ≥ 50%) or PaO₂ > 70 (if FiO₂ < 50%) = 0 points, PaO₂ 61-70 = +1 point, PaO₂ 55-60 = +3 points, PaO₂ < 55 = +4 points.
8. Arterial pH: ≥7.7 = +4 points, 7.60 to <7.70 = +3 points, 7.50 to <7.60 = +1 point, 7.33 to <7.50 = 0 points, 7.25 to <7.33 = +2 points, 7.15 to <7.25 = +3 points, <7.15 = +4 points
9. Serum sodium, mmol/L: ≥180 = +4 points, 160 to <180 = +3 points, 155 to <160 = +2 points, 150 to <155 = +1 point, 130 to <150 = 0 points, 120 to <130 = +2 points, 111 to <120 = +3 points, <111 = +4 points
10. Serum potassium, mmol/L: ≥7.0 = +4 points, 6.0 to <7.0 = +3 points, 5.5 to <6.0 = +1 point, 3.5 to <5.5 = 0 points, 3.0 to <3.5 = +1 point, 2.5 to <3.0 = +2 points, <2.5 = +4 points
11. Serum creatinine, mg/100 mL: ≥3.5 and ACUTE renal failure = +8 points, 2.0 to <3.5 and ACUTE renal failure = +6 points, ≥3.5 and CHRONIC renal failure = +4 points, 1.5 to <2.0 and ACUTE renal failure = +4 points, 2.0 to <3.5 and CHRONIC renal failure = +3 points, 1.5 to <2.0 and CHRONIC renal failure = +2 points, 0.6 to <1.5 = 0 points, <0.6 = +2 points
12. Hematocrit, %: ≥60 = +4 points, 50 to <60 = +2 points, 46 to <50 = +1 point, 30 to <46 = 0 points, 20 to <30 = +2 points, <20 = +4 points
13. White blood count, total/cubic mm in 10^3: ≥40 = +4 points, 20 to <40 = +2 points, 15 to <20 = +1 point, 3 to <15 = 0 points, 1 to <3 = +2 points, <1 = +4 points
14. Glasgow Coma Scale (GCS): 1-15 points (use 15 - [GCS Score])

The total APACHE II score is calculated by summing the points for each criterion.
    """
    
    explanation += "\nThe patient's current APACHE II score is 0 points.\n"
    score = 0

    sodium_exp, sodium = unit_converter_new.conversion_explanation(input_parameters['sodium'][0], "sodium", 22.99, 1, input_parameters['sodium'][1], "mmol/L")
    pH = input_parameters['pH']
    heart_rate = input_parameters['heart_rate'][0]
    respiratory_rate = input_parameters['respiratory_rate'][0]
    potassium_exp, potassium = unit_converter_new.conversion_explanation(input_parameters['potassium'][0], "potassium", 39.10, 1, input_parameters['potassium'][1], "mmol/L")
    creatinine_exp, creatinine = unit_converter_new.conversion_explanation(input_parameters['creatinine'][0], "creatinine", 113.12, None, input_parameters['creatinine'][1], "mg/dL")
    acute_renal_failure = input_parameters.get('acute_renal_failure', False)
    chronic_renal_failure = input_parameters.get('chronic_renal_failure', False)
    hematocrit =  input_parameters['hematocrit'][0]
    wbc_exp, wbc = unit_converter_new.convert_to_units_per_liter_explanation(input_parameters['wbc'][0], input_parameters['wbc'][1], "white blood cell count", "L") 
    fio2 = input_parameters['fio2'][0]
    gcs = int(input_parameters['gcs'])
    a_a_gradient = input_parameters.get('a_a_gradient', False)
    partial_pressure_oxygen = input_parameters.get('pao2', False)

    age_explanation, age = age_conversion.age_conversion_explanation(input_parameters['age'])

    explanation += f"{age_explanation}"

    if age < 45:
        explanation += f"Because the patient's age is less than 45, no points are added to the score, keeping it at {score}."
    elif 45 < age <= 54:
        explanation += f"Because the patient's age is between 45 and 54, 2 points are added to the total, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 55 <= age <= 64:
        explanation += f"Because the patient's age is between 55 and 64, 3 points are added to the total, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 65 <= age <= 74:
        explanation += f"Because the patient's age is between 65 and 74, 5 points are added to the total, making the current total, {score} + 5 = {score + 5}.\n"
        score += 5
    elif age >= 75:
        explanation += f"Because the patient's age is at least 75 years, 6 points are added to the total, making the current total, {score} + 6 = {score + 6}.\n"
        score += 6

    if 'severe_organ_failure_or_immunocompromise' in input_parameters:
        if input_parameters['severe_organ_failure_or_immunocompromise']:

            surgery_type = input_parameters.get('surgery_type', None)

            explanation += f"The patient is reported to have an organ failure of immunocompromise with a surgery type being classified as {surgery_type}. "

            if surgery_type == "Nonelective":
                explanation += f"The patient's surgery type is classified as 'Nonelective' and so 0 points are added to the total, keeping the total at {score} points.\n"
            elif surgery_type == "Elective":
                explanation += f"The patient's surgery type is classified as 'Elective' and so 2 points are added to the total, making the current total {score} + 2 = {score + 2}.\n"
                score += 2
            elif surgery_type == "Emergency":
                explanation += f"The patient's surgery type is classified as 'Emergency' and so 5 points are added to the total, making the current total {score} + 5 = {score + 5}.\n"
                score += 5
        elif not input_parameters['severe_organ_failure_or_immunocompromise']:
            explanation += f"The patient is reported to not have any organ failure immunocompromise and so 0 points are added to the total, keeping the total at {score} points.\n"
    else:
        explanation += f"The patient note does not report any history on immunocompromise and so we assume this to be false. Hence, 0 points are added to the total, keeping the total at {score} points.\n"
    
    explanation += f"The patient's FiO2 percentage is {fio2}%.\n"

    if fio2 >= 50:
        explanation += "Because the patient's FiO₂ percentage is 50% or greater, we need to examine the A-a gradient to compute the APACHE II score. "
        a_a_gradient = input_parameters['a_a_gradient']
        explanation += f"The patient's A-a gradient is {a_a_gradient}. "
        if a_a_gradient > 499:
            explanation += f"Because the patient's A-a gradient is greater than 499, we add 4 points to the total, making the current total {score} + 4 = {score + 4}.\n"
            score += 4
        elif 350 <= a_a_gradient <= 499:
            explanation += f"Because the patient's A-a gradient is between 350 and 499, we add 3 points to the total, making the current total {score} + 3 = {score + 3}.\n"
            score += 3
        elif 200 <= a_a_gradient <= 349:
            explanation += f"Because the patient's A-a gradient is between 200 and 349, we add 2 points to the total, making the current total {score} + 2 = {score + 2}.\n"
            score += 2
        else:  
            explanation += f"Because the patient's A-a gradient is less than 200, we do not add any points to the total, keeping the current total at {score}.\n"

    else:
        partial_pressure_oxygen = input_parameters['pao2'][0]
        explanation += "Because the patient's FiO₂ percentage is less than 50%, we need to examine the patient's partial pressure of oxygen (PaO₂) to compute the APACHE II score. "
        explanation += f"The patient's PaO₂ is {partial_pressure_oxygen} mm Hg. "
        if partial_pressure_oxygen > 70:
            explanation += f"Because the patient's PaO₂ is greater than 70 mm Hg, we do not add any points to the total, keeping the current total at {score}.\n"
        elif 61 <= partial_pressure_oxygen <= 70:
            explanation += f"Because the patient's PaO₂ is between 61 and 70 mm Hg, we add 1 point to the total, making the current total {score} + 1 = {score + 1}.\n"
            score += 1
        elif 55 <= partial_pressure_oxygen <= 60:
            explanation += f"Because the patient's PaO₂ is between 55 and 60 mm Hg, we add 3 points to the total, making the current total {score} + 3 = {score + 3}.\n"
            score += 3
        else: 
            explanation += f"Because the patient's PaO₂ is less than 55 mm Hg, we add 4 points to the total, making the current total {score} + 4 = {score + 4}.\n"
            score += 4

    temperature_explanation, temperature = convert_temperature.fahrenheit_to_celsius_explanation(input_parameters["temperature"][0], input_parameters["temperature"][1])

    explanation += temperature_explanation + "\n"

    if temperature >= 41:
        explanation += f"Because the patient's temperature is {temperature} degrees celsius or higher, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 39 <= temperature < 41:
        explanation += f"Because the patient's temperature is between 39 and 41 degrees celsius, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 38.5 <= temperature < 39:
        explanation += f"Because the patient's temperature is between 38.5 and 39 degrees celsius, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 36 <= temperature < 38.5:
        explanation += f"Because the patient's temperature is between 36 and 38.5 degrees celsius, no points are added to the score, keeping the current total at {score}.\n"
    elif 34 <= temperature < 36:
        explanation += f"Because the patient's temperature is between 34 and 36 degrees celsius, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 32 <= temperature < 34:
        explanation += f"Because the patient's temperature is between 32 and 34 degrees celsius, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 30 <= temperature < 32:
        explanation += f"Because the patient's temperature is between 30 and 32 degrees celsius, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif temperature < 30:
        explanation += f"Because the patient's temperature is below 30 degrees celsius, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    else:
        explanation += f"The patient's temperature is within the normal range, so no additional points are added to the score, keeping the total at {score}.\n"

    map_exp = mean_arterial_pressure.mean_arterial_pressure_explanation(input_parameters)

    explanation += map_exp["Explanation"]

    map_value = map_exp["Answer"]
    
    # Mean Arterial Pressure (MAP)
    if map_value > 159:
        explanation += f"Because the patient's mean arterial pressure is above 159 mmHg, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 129 < map_value <= 159:
        explanation += f"Because the patient's mean arterial pressure is between 130 and 159 mmHg, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 109 < map_value <= 129:
        explanation += f"Because the patient's mean arterial pressure is between 110 and 129 mmHg, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 69 < map_value <= 109:
        explanation += f"Because the patient's mean arterial pressure is between 70 and 109 mmHg, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 49 < map_value <= 69:
        explanation += f"Because the patient's mean arterial pressure is between 50 and 69 mmHg, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif map_value <= 49:
        explanation += f"Because the patient's mean arterial pressure is 49 mmHg or lower, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4

    explanation += f"The patient's heart rate is {heart_rate} beats per minute.\n"

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
    elif 55 <= heart_rate < 70:
        explanation += f"Because the patient's heart rate is between 55 and 69 beats per minute, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif 40 <= heart_rate < 55:
        explanation += f"Because the patient's heart rate is between 40 and 54 beats per minute, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif heart_rate < 40:
        explanation += f"Because the patient's heart rate is less than 40 beats per minute, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4


    explanation += f"The patient's respiratory rate is {respiratory_rate} breaths per minute.\n"

    # Respiratory Rate
    if respiratory_rate >= 50:
        explanation += f"Because the patient's respiratory rate is 50 breaths per minute or more, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4
    elif 35 <= respiratory_rate < 50:
        explanation += f"Because the patient's respiratory rate is between 35 and 49 breaths per minute, 3 points are added to the score, making the current total, {score} + 3 = {score + 3}.\n"
        score += 3
    elif 25 <= respiratory_rate < 35:
        explanation += f"Because the patient's respiratory rate is between 25 and 34 breaths per minute, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 12 <= respiratory_rate < 25:
        explanation += f"Because the patient's respiratory rate is between 12 and 24 breaths per minute, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 10 <= respiratory_rate < 12:
        explanation += f"Because the patient's respiratory rate is between 10 and 11 breaths per minute, 1 point is added to the score, making the current total, {score} + 1 = {score + 1}.\n"
        score += 1
    elif 6 <= respiratory_rate < 10:
        explanation += f"Because the patient's respiratory rate is between 6 and 9 breaths per minute, 2 points are added to the score, making the current total, {score} + 2 = {score + 2}.\n"
        score += 2
    elif respiratory_rate < 6:
        explanation += f"Because the patient's respiratory rate is less than 6 breaths per minute, 4 points are added to the score, making the current total, {score} + 4 = {score + 4}.\n"
        score += 4


    explanation += f"The patient's pH is {pH}.\n"

    # pH Levels
    if pH >= 7.70:
        explanation += f"Because the patient's pH is above 7.70, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 7.60 <= pH < 7.70:
        explanation += f"Because the patient's pH is between 7.60 and 7.69, 3 points are added to the score, making the current total {score} + 3 = {score + 3}.\n"
        score += 3
    elif 7.50 <= pH < 7.60:
        explanation += f"Because the patient's pH is between 7.50 and 7.59, 1 point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 7.33 <= pH < 7.50:
        explanation += f"Because the patient's pH is between 7.33 and 7.49, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 7.25 <= pH < 7.33:
        explanation += f"Because the patient's pH is between 7.25 and 7.32, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 7.15 <= pH < 7.25:
        explanation += f"Because the patient's pH is between 7.15 and 7.24, 3 points are added to the score, making the current total {score} + 3 = {score + 3}.\n"
        score += 3
    elif pH < 7.15:
        explanation += f"Because the patient's pH is below 7.15, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4


    explanation += sodium_exp

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
        explanation += f"Because the patient's sodium level is between 150 and 154 mmol/L, 1 point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 130 <= sodium < 150:
        explanation += f"Because the patient's sodium level is between 130 and 149 mmol/L, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 120 <= sodium < 130:
        explanation += f"Because the patient's sodium level is between 120 and 129 mmol/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 111 <= sodium < 120:
        explanation += f"Because the patient's sodium level is between 111 and 119 mmol/L, 3 points are added to the score, making the current total {score} + 3 = {score + 3}.\n"
        score += 3
    elif sodium < 111:
        explanation += f"Because the patient's sodium level is below 111 mmol/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4

    explanation += potassium_exp

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
        explanation += f"Because the patient's potassium level is between 3.5 and 5.4 mmol/L, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 3.0 <= potassium < 3.5:
        explanation += f"Because the patient's potassium level is between 3.0 and 3.4 mmol/L, 1 point is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 2.5 <= potassium < 3.0:
        explanation += f"Because the patient's potassium level is between 2.5 and 2.9 mmol/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif potassium < 2.5:
        explanation += f"Because the patient's potassium level is below 2.5 mmol/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4

    explanation += creatinine_exp

    if acute_renal_failure:
        explanation += "The patient is determined to have an acute renal failure.\n"
    else:
        explanation += "The patient is determined to not have an acute renal failure.\n"

    if chronic_renal_failure:
        explanation += "The patient is determined to have a chronic renal failure.\n"
    else:
        explanation += "The patient is determined to not have a chronic renal failure.\n"

    # Creatinine Levels
    if creatinine >= 3.5 and acute_renal_failure:
        additional_points = 8
        explanation += f"Because the patient has acute renal failure and a creatinine level above 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and acute_renal_failure:
        additional_points = 6
        explanation += f"Because the patient has acute renal failure and a creatinine level between 2.0 and 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif creatinine >= 3.5 and chronic_renal_failure:
        additional_points = 4
        explanation += f"Because the patient has chronic renal failure and a creatinine level above 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 2.0 <= creatinine < 3.5 and chronic_renal_failure:
        additional_points = 3
        explanation += f"Because the patient has chronic renal failure and a creatinine level between 2.0 and 3.5, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and acute_renal_failure:
        additional_points = 4
        explanation += f"Because the patient has acute renal failure and a creatinine level between 1.5 and 2.0, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 1.5 <= creatinine < 2.0 and chronic_renal_failure:
        additional_points = 2
        explanation += f"Because the patient has chronic renal failure and a creatinine level between 1.5 and 2.0, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points
    elif 0.6 <= creatinine < 1.5:
        explanation += f"Because the patient's creatinine level is between 0.6 and 1.4, no points are added to the score, keeping the current total at {score}.\n"
    elif creatinine < 0.6:
        additional_points = 2
        explanation += f"Because the patient's creatinine level is below 0.6, {additional_points} points are added to the score, making the current total {score} + {additional_points} = {score + additional_points}.\n"
        score += additional_points


    explanation += f"The patient has a hematocrit of {hematocrit}%.\n"

    # Hematocrit Levels
    if hematocrit >= 60:
        explanation += f"Because the patient's hematocrit is 60% or higher, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 50 <= hematocrit < 60:
        explanation += f"Because the patient's hematocrit is between 50% and 59%, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 46 <= hematocrit < 50:
        explanation += f"Because the patient's hematocrit is between 46% and 49%, 1 points is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 30 <= hematocrit < 46:
        explanation += f"Because the patient's hematocrit is between 30% and 45%, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 20 <= hematocrit < 30:
        explanation += f"Because the patient's hematocrit is between 20% and 30%, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif hematocrit < 20:
        explanation += f"Because the patient's hematocrit is less than 20%, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4

    explanation += wbc_exp

    # WBC Count
    if wbc >= 40e9:
        explanation += f"Because the patient's white blood cell count is above 40x10^9/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4
    elif 20e9 <= wbc < 40e9:
        explanation += f"Because the patient's white blood cell count is at least 20x10^9/L, but less than 40 x10^9/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif 15e9 <= wbc < 20e9:
        explanation += f"Because the patient's white blood cell count is at least 15x10^9/L, but less than 20 x10^9/L, 1 points is added to the score, making the current total {score} + 1 = {score + 1}.\n"
        score += 1
    elif 3e9 <= wbc < 15e9:
        explanation += f"Because the patient's white blood cell count is at least 3x10^9/L, but less than 15 x10^9/L, 0 points are added to the patient's score, keeping the total at {score}.\n"
    elif 10e9 <= wbc < 3e9:
        explanation += f"Because the patient's white blood cell count is at least 1x10^9/L, but less than 3 x10^9/L, 2 points are added to the score, making the current total {score} + 2 = {score + 2}.\n"
        score += 2
    elif wbc < 1e9:
        explanation += f"Because the patient's white blood cell count is less than 1x10^9/L, 4 points are added to the score, making the current total {score} + 4 = {score + 4}.\n"
        score += 4

    # Glasgow Coma Score
    apache_ii_gcs = int(15 - gcs)
    explanation += f"The patient's Glasgow Coma Score is {gcs}. For this criterion, we subtract 15 from the {gcs} points and add that to the total score. 15 - {gcs} = {apache_ii_gcs}. Hence, we add {apache_ii_gcs} to the total making the current total {apache_ii_gcs} + {score} = {apache_ii_gcs + score}.\nHence, the patient's APACHE II score is {apache_ii_gcs + score}."
    score += apache_ii_gcs

    return {"Explanation": explanation, "Answer": score}


