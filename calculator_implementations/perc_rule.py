import age_conversion

def compute_perc_rule_explanation(input_parameters):

    perc_count = 0

    explanation = "The current count of PERC criteria met is 0.\n"

    age_exp, age = age_conversion.age_conversion_explanation(input_parameters["age"])
    heart_rate = input_parameters["heart_rate"][0]
    oxygen_sat = input_parameters["oxygen_sat"][0]

    parameters = {"unilateral_leg_swelling": "unilateral leg swelling", "hemoptysis": "hemoptysis", "recent_surgery_or_trauma": "recent surgery or trauma", 
                  "previous_pe": "prior pulmonary embolism", "previous_dvt": "prior deep vein thrombosis", "hormonal_use": "hormonal use"}
    
    explanation += age_exp
    if age >= 50:
        explanation += f"The patient's age is greater than or equal to 50 years, and so we increment the perc critieria met by 1, making the current total {perc_count} + 1 = {perc_count + 1}.\n"
        perc_count += 1
    else:
        explanation += f"The patient's age is less than 50 years, and so we do not increment the criteria count. The current total remains at {perc_count}.\n"


    explanation += f"The patient's heart rate is {heart_rate} beats per minute. "

    if heart_rate >= 100:
        explanation += f"The patient's heart rate is greater than or equal to 100 beats per minute, and so we increment the perc critieria met by 1, making the current total {perc_count} + 1 = {perc_count + 1}.\n"
        perc_count += 1
    else:
        explanation += f"The patient's heart rate is less than 100 beats per minute, and so we do not increment the criteria count. The current total remains at {perc_count}.\n"


    explanation += f"The saturated oxygen percentage in the room is {oxygen_sat} percent. " 

    if oxygen_sat < 95:
        explanation += f"The saturated oxygen is less than 95%, and so we increment the perc critieria met by 1, making the current total {perc_count} + 1 = {perc_count + 1}.\n"
        perc_count += 1
    else:
        explanation += f"The saturated oxygen is greater than or equal to 95% and so we do not increment the criteria count. The current total remains at {perc_count}.\n"
    

    for parameter in parameters:

        if parameter == "previous_pe":
            continue
        
        if parameter == "previous_dvt":
            explanation += "The patient must be diagnosed with at least one of deep vein thrombosis or pulmonary embolism in the past for a PERC rule criteria to be met. "
        
            if 'previous_dvt' not in input_parameters:
                explanation += "Whether the patient has been diagnosed for pulmonary embolism in the past is not reported. Hence, we assume it to be absent. "
                input_parameters['previous_dvt'] = False 
            elif not input_parameters['previous_dvt']:
                explanation += "The patient is not reported to have been diagnosed with deep vein thrombosis in the past. "
            else:
                explanation += "The patient is reported to have been diagnosed with deep vein thrombosis in the past. "

            if 'previous_pe' not in input_parameters:
                explanation += "Whether the patient has been diagnosed for pulmonary embolism in the past is not reported. Hence, we assume it to be absent. "
                input_parameters['previous_pe'] = False
            elif not input_parameters['previous_pe']:
                explanation += "The patient is not reported to have been diagnosed with pulmonary embolism in the past. "
            else:
                explanation += "The patient is reported to have been diagnosed with pulmonary embolism in the past. "

            if input_parameters['previous_dvt'] or input_parameters['previous_pe']:
                explanation += f"At least one of the criteria is met and so we increment the criteria met by 1, making the current total {perc_count} + 1 = {perc_count + 1}.\n"
                perc_count += 1
            else:
                explanation += f"Neither criteria is met and so we do increment the criteria count, keep the current total at {perc_count}.\n"
            continue

        if parameter not in input_parameters:
            explanation += f"The patient note does not report a status on '{parameters[parameter]}'. Hence, we assume it to be absent, and so we do not increment the criteria count. The current total remains at {perc_count}.\n"
        elif not input_parameters[parameter]:
            explanation += f"The patient note reports '{parameters[parameter]}' to be absent in the patient and so we do not increment the criteria count. The current total remains at {perc_count}.\n"
        else:
            explanation += f"The patient note reports '{parameters[parameter]}' to be present for the patient and so we increment the criteria count by 1, making the current total {perc_count} + 1  =  {perc_count + 1}.\n"
            perc_count += 1

    explanation += f"Hence, the number of PERC rule criteria met by the patient is {perc_count}.\n"

    return {"Explanation": explanation, "Answer": perc_count}
