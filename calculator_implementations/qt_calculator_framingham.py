from rounding import round_number


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

    explanation += f"The patient's corrected QT interval (QTc) is {qt_c} msec."

    return {"Explanation": explanation, "Answer": qt_c}

