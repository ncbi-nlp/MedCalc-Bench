import unit_converter_new
import age_conversion
import math
from rounding import round_number

def framingham_risk_score_explanation(input_parameters):


    explanation = ("For males, the formula for computing the Framingham Risk Score is:\n52.00961 * ln(age) + 20.014077 * ln(total_cholesterol) + -0.905964 * ln(hdl_cholesterol) + 1.305784 * ln(sys_bp) + 0.241549 * bp_medicine + 12.096316 * smoker + -4.605038 * ln(age) * ln(total_cholesterol) + -2.84367 * ln(age_smoke) * smoker + -2.93323 * ln(age) * ln(age) - 172.300168.\n")
    

    explanation += ("The patient's age is capped at 70 for the ln(age_smoke) * smoker term if greater than 70. The 10-year risk percentage is calculated as: [1 - 0.9402^exp(risk_score)] * 100.\n")
    
    explanation += ("For females, the formula for computing the Framingham Risk Score is:\n31.764001 * ln(age) + 22.465206 * ln(total_cholesterol) + -1.187731 * ln(hdl_cholesterol) + 2.552905 * ln(sys_bp) + 0.420251 * bp_medicine + 13.07543 * smoker + -5.060998 * ln(age) * ln(total_cholesterol) + -2.996945 * ln(age_smoke) * smoker - 146.5933061.\n")
    

    explanation += ("The patient's age is capped at 78 for the ln(age_smoke) * smoker term if greater than 78. The 10-year risk percentage is calculated as: [1 - 0.98767^exp(risk_score)] * 100.\n")
        


    age = input_parameters["age"]
    gender = input_parameters["sex"]
    explanation += f"The patient's gender is {gender}.\n"

    age_explanation, age = age_conversion.age_conversion_explanation(input_parameters["age"])

    explanation += age_explanation

    # Cap age for specific terms
    age_smoke = min(age, 70 if gender == "Male" else 78)
    explanation += f"The patient's age is {age}, and the adjusted age for smoking-related terms is {age_smoke}.\n"

    # Smoker variable

    if "smoker" not in input_parameters:
        explanation += "The patient's smoking status is not provided, so the smoker variable is set to 0.\n"
        smoker = 0
    else:
        smoker = 1 if input_parameters["smoker"] else 0
        explanation += f"The patient is {'a smoker' if smoker else 'not a smoker'}, so the smoker variable is {smoker}.\n"

    if "bp_medicine" not in input_parameters:
        explanation += "The information for whether the patient is taking medicine for blood pressure is not provided, so the bp_medicine variable is set to 0.\n"
        bp_medicine = 0
    else:
        bp_medicine = 1 if input_parameters["bp_medicine"] else 0
        explanation += f"The patient is {'on' if bp_medicine else 'not on'} medication for blood pressure, so the bp_medicine variable is {bp_medicine}.\n"

    # Cholesterol and blood pressure variables
    total_cholesterol = input_parameters["total_cholesterol"]
    hdl_cholesterol = input_parameters["hdl_cholesterol"]
    sys_bp = input_parameters["sys_bp"][0]

    total_cholesterol_exp, total_cholesterol = unit_converter_new.conversion_explanation(total_cholesterol[0], 386.654, "total cholesterol", None, total_cholesterol[1], "mg/dL")
    hdl_cholesterol_exp, hdl_cholesterol = unit_converter_new.conversion_explanation(hdl_cholesterol[0], "hdl cholesterol", 386.654, None, hdl_cholesterol[1], "mg/dL")

    explanation += total_cholesterol_exp
    explanation += hdl_cholesterol_exp
    explanation += f"The patient's systolic blood pressure is {sys_bp} mm Hg.\n"


    ln_age = math.log(age)
    ln_total_cholesterol = math.log(total_cholesterol)
    ln_hdl_cholesterol = math.log(hdl_cholesterol)
    ln_sys_bp = math.log(sys_bp)
    ln_age_smoke = math.log(age_smoke)


    coefficients = {
        "Male": {
            "ln_age": 52.00961,
            "ln_total_cholesterol": 20.014077,
            "ln_hdl_cholesterol": -0.905964,
            "ln_sys_bp": 1.305784,
            "bp_medicine": 0.241549,
            "smoker": 12.096316,
            "ln_age_ln_total_cholesterol": -4.605038,
            "ln_age_smoker": -2.84367,
            "ln_age_ln_age": -2.93323,
            "constant": -172.300168
        },
        "Female": {
            "ln_age": 31.764001,
            "ln_total_cholesterol": 22.465206,
            "ln_hdl_cholesterol": -1.187731,
            "ln_sys_bp": 2.552905,
            "bp_medicine": 0.420251,
            "smoker": 13.07543,
            "ln_age_ln_total_cholesterol": -5.060998,
            "ln_age_smoker": -2.996945,
            "ln_age_ln_age": 0,  # Not applicable for women
            "constant": -146.5933061
        }
    }
    beta = coefficients[gender]

    # Risk score calculation
    risk_score = (
        beta["ln_age"] * ln_age +
        beta["ln_total_cholesterol"] * ln_total_cholesterol +
        beta["ln_hdl_cholesterol"] * ln_hdl_cholesterol +
        beta["ln_sys_bp"] * ln_sys_bp +
        beta["bp_medicine"] * bp_medicine +
        beta["smoker"] * smoker +
        beta["ln_age_ln_total_cholesterol"] * ln_age * ln_total_cholesterol +
        beta["ln_age_smoker"] * ln_age_smoke * smoker +
        beta["ln_age_ln_age"] * ln_age * ln_age +
        beta["constant"]
    )

    if gender == "Male":
        risk_percentage = 1 - 0.9402 ** math.exp(risk_score)
    else:
        risk_percentage = 1 - 0.98767 ** math.exp(risk_score)
    risk_percentage *= 100

    if gender == "Female":
        explanation += f"Plugging in the values into the risk score formula, we get 31.764001 * ln({age}) + 22.465206 * ln({total_cholesterol}) + -1.187731 * ln({hdl_cholesterol}) + 2.552905 * ln({sys_bp}) + 0.420251 * {bp_medicine} + 13.07543 * {smoker} + -5.060998 * ln({age}) * ln({total_cholesterol}) + -2.996945 * ln({age_smoke}) * {smoker} - 146.5933061 = {risk_score:.3f}.\n"
        explanation += f"To obtain the 10-year risk percentage, we plug this into the formula as: [1 - 0.98767^exp(risk_score)] * 100 = {risk_percentage}.\n"
    else:
        explanation += f"Plugging in the values into the risk score formula, we get 52.00961 * ln({age}) + 20.014077 * ln({total_cholesterol}) + -0.905964 * ln({hdl_cholesterol}) + 1.305784 * ln({sys_bp}) + 0.241549 * {bp_medicine} + 12.096316 * {smoker} + -4.605038 * ln({age}) * ln({total_cholesterol}) + -2.84367 * ln({age_smoke}) * {smoker} + -2.93323 * ln({age}) * ln({age}) - 172.300168 = {risk_score:.3f}.\n"
        explanation += f"To obtain the 10-year risk percentage, we plug this into the formula as: [1 - 0.9402^exp(risk_score)] * 100 = {risk_percentage}.\n"

    explanation += f"Hence, the patient's 10-year risk percentage of MI or death is {risk_percentage:.3f}%."
    
    return {"Explanation": explanation, "Answer": round(risk_percentage, 3)}


