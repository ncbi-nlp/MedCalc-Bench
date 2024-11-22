import unit_converter_new

def glasgow_bleeding_score_explanation(input_parameters):

    explanation = """
    The criteria for the Glasgow-Blatchford Score are listed below:

    1. BUN (mg/dL): <18.2 = 0 points, 18.2-22.3 = +2 points, 22.4-28 = +3 points, 28-70 = +4 points, >70 = +6 points
    2. Hemoglobin (g/dL) for men: >=13 = 0 points, <=12-13 = +1 point, <=10-12 = +3 points, <10 = +6 points
    3. Hemoglobin (g/dL) for women: >=12 = 0 points, <=10-12 = +1 point, <10 = +6 points
    4. Systolic blood pressure (mm Hg): ≥110 = 0 points, 100-109 = +1 point, 90-99 = +2 points, <90 = +3 points
    5. Pulse ≥100 (per minute): No = 0 points, Yes = +1 point
    6. Melena present: No = 0 points, Yes = +1 point
    7. Presentation with syncope: No = 0 points, Yes = +1 point
    8. Liver disease history: No = 0 points, Yes = +1 point
    9. Cardiac failure present: No = 0 points, Yes = +1 point

    The total Glasgow-Blatchford Score is calculated by summing the points for each criterion.
    """

    score = 0

    hemoglobin_exp, hemoglobin = unit_converter_new.conversion_explanation(input_parameters["hemoglobin"][0], "hemoglobin", 64500, None, input_parameters["hemoglobin"][1], "g/dL")
    bun_exp, bun = unit_converter_new.conversion_explanation(input_parameters["bun"][0], "BUN", 28.08, None, input_parameters["bun"][1], "mg/dL")
    gender = input_parameters["sex"]
    systiolic_bp = input_parameters["sys_bp"][0]
    heart_rate = input_parameters["heart_rate"][0]
    
    explanation += f"The current glasgow bleeding score is 0. The patient's gender is {gender}.\n"
    explanation += hemoglobin_exp 

    if gender == "Male":
        if 12 <= hemoglobin < 13:
            explanation += f"Because the patient is a male and his hemoglobin concentration is greater than or equal to 12 g/dL, but less than 13 g/dL, we add one point, making the current score {score} + 1 = {score + 1}.\n"
            score += 1
        elif 10 <= hemoglobin < 12:
            explanation += f"Because the patient is a male and his hemoglobin concentration is greater than or equal to 10 g/dL, but less than 12 g/dL, we add three points, making the current score {score} + 3 = {score + 3}.\n"
            score += 3
        elif hemoglobin < 10:
            explanation += f"Because the patient is a male and his hemoglobin concentration is less than 10 and 12 g/dL, we add six points, making the current score {score} + 6 = {score + 6}.\n"
            score += 6
        elif hemoglobin >= 13:
            explanation += f"Because the patient is a male and his hemoglobin concentration is greater than or equal to 13 g/dL, we do not add any points, keeping the current score at {score}.\n"

    else:
        if 10 <= hemoglobin < 12:
            explanation += f"Because the patient is a female and her hemoglobin concentration is greater than or equal to 10 g/dL, but less than 12 g/dL, we add one point, making the current score {score} + 1 = {score + 1}.\n"
            score += 1
        elif hemoglobin < 10:
            explanation += f"Because the patient is a female and her hemoglobin concentration is less than 10 mg/dL, we add six points, making the current score {score} + 6 = {score + 6}.\n"
            score += 6
        elif hemoglobin >= 12:
            explanation += f"Because the patient is a female and her hemoglobin concentration is greater than or equal to 12 mg/dL, we do not add any points, keeping the current score at {score}.\n"

    explanation += bun_exp

    if 18.2 <= bun < 22.4:
        explanation += f"The BUN concentration is greater than equal to 18.2 mg/dL, but less than 22.4 mg/dL, and so we add two points, making the current score {score} + 2 = {score + 2}.\n"
        score += 2
    elif 22.4 <= bun < 28:
        explanation += f"The BUN concentration is greater than equal to 22.4 mg/dL, but less than 28 mg/dL, and so we add three points, making the current score {score} + 3 = {score + 3}.\n"
        score += 3
    elif 28 <= bun <= 70:
        explanation += f"The BUN concentration is between 28 and 70 mg/dL, and so we add four points, making the current score {score} + 4 = {score + 4}.\n"
        score += 4
    elif bun > 70:
        explanation += f"The BUN concentration is greater than 70 mg/dL, and so we add six points, making the current score {score} + 6 = {score + 6}.\n"
        score += 6
    elif bun < 18.2:
        explanation += f"The BUN concentration is less than 18.2 mg/dL, and so we do not make any changes to the score, keeping the score at {score}.\n"

    explanation += f"The patient's blood pressure is {systiolic_bp} mm Hg. "

    if 100 <= systiolic_bp < 110:
        explanation += f"Because the patient's systolic blood pressure is greater than or equal to 100 mm Hg, but less than 110 mm Hg, we increase the score by one point, making the current score {score} + 1 = {score + 1}.\n"
        score += 1
    elif 90 <= systiolic_bp < 100:
        explanation += f"Because the patient's systolic blood pressure is greater than or equal to 90 mm Hg, but less than 100 mm Hg, we increase the score by two points, making the current score {score} + 2 = {score + 2}.\n"
        score += 2
    elif systiolic_bp < 90:
        explanation += f"Because the patient's systolic blood pressure is less than 90 mm Hg, we increase the score by three points, making the current score {score} + 3 = {score + 3}.\n"
        score += 3
    elif systiolic_bp >= 110:
        explanation += f"Because the patient's systolic blood pressure is greater than or equal to 110 mm Hg, we do not add points to the score, keeping the current score at {score}.\n"


    explanation += f"The patient's heart rate is {heart_rate} beats per minute. "

    if heart_rate >= 100:
        explanation += f"Because the heart rate is greater or equal to than 100 beats per minute, we increase the score by one point, making the current score {score} + 1 = {score + 1}.\n"
        score += 1
    else:
         explanation += f"Because the heart rate is less than 100 beats per minute, we do not change the score, keeping the current score at {score}.\n"


    default_parameters = {"melena_present": "melena", "syncope": "recent syncope", "hepatic_disease_history": "hepatic disease history", "cardiac_failure": "cardiac failure"}

    for parameter in default_parameters:
        if parameter not in input_parameters:
            explanation += f"The patient's status for {default_parameters[parameter]} is missing from the patient note and so we assume it is absent from the patient.\n"
            input_parameters[parameter] = False
            explanation += f"Hence, we do not add any points to the score, keeping it at {score}.\n"
        
        elif parameter in ['syncope', 'hepatic_disease_history', 'cardiac_failure'] and input_parameters[parameter]:
            explanation +=  f"The patient has a {default_parameters[parameter]}, and so we add two points to the current total, making the current total {score} + 2 =  {score + 2}.\n"
            score += 2
            
        elif input_parameters[parameter]:
            explanation +=  f"The patient has {default_parameters[parameter]} and so we add one point to the current total, making the current total {score} + 1 =  {score + 1}.\n"
            score += 1
       
        else:
            explanation +=  f"The patient's status for {default_parameters[parameter]} is reported to be absent for the patient, and so we do not add any points, keeping the current total at {score}.\n"
        
    explanation += f"The patient's Glasgow Bleeding Score is {score}.\n"

    return {"Explanation": explanation, "Answer": score}
