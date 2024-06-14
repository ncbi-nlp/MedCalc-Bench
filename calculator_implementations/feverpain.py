def compute_fever_pain_explanation(input_parameters):

    parameter_name = {"fever_24_hours": "a fever in the past 24 hours", "cough_coryza_absent": "an absence of cough or coryza", 
                      "symptom_onset": "a symptom onset ≤3 days", "purulent_tonsils": "purulent tonsils", "severe_tonsil_inflammation": "severe tonsil inflammation"}
    
    fever_pain_score = 0

    explanation = "The patient's current FeverPain score is 0.\n"

    for parameter in parameter_name:

        if parameter not in input_parameters:
            explanation += f"Whether the patient has {parameter_name[parameter]} is not reported and so we assume that it is absent for the patient. Because of this, we do not increment the score, keeping the current total at {fever_pain_score}.\n"
        
        elif input_parameters[parameter]:
            explanation += f"'The patient is reported to have {parameter_name[parameter]} and so we increment the score by 1, making the current total {fever_pain_score} + 1 = {fever_pain_score + 1}.\n"
            fever_pain_score += 1

        else:
            explanation += f"The patient is reported to not have {parameter_name[parameter]} and so we do not increment the score, keeping the current total at {fever_pain_score}.\n"

    explanation += f"The patient's FeverPain score is {fever_pain_score} points.\n"

    return {"Explanation": explanation, "Answer": fever_pain_score}

