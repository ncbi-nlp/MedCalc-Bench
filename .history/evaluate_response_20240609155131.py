import json
import os
from openai import AzureOpenAI
import argparse
import pandas as pd
import sys
import math
import tqdm 
import re 

client = AzureOpenAI(
	api_version="2024-03-01-preview",
	azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
	api_key=os.getenv("OPENAI_API_KEY"),
)



def extract_answer(answer): # previous extract_answer function for outputs
    extracted_answer = re.findall(r'[Aa]nswer"*:\s*(.*?)\}', answer)
    if len(extracted_answer) == 0:
        extracted_answer = "not found"
    else:
        extracted_answer = extracted_answer[-1].strip().strip('"')
        if extracted_answer == "str(short_and_direct_answer_of_the_question)" or extracted_answer == "str(value which is the answer to the question)" or extracted_answer == "X.XX":
            extracted_answer = "not found"
    return extracted_answer


def clean_answer(raw_answer, ground_truth, calid, upper_limit, lower_limit):
    raw_answer = extract_answer(raw_answer) # call extract_answer function above for a rough extraction
    return check_correctness(raw_answer, ground_truth, calid, upper_limit, lower_limit)
    
def check_correctness(raw_answer, ground_truth, calid, upper_limit, lower_limit):
    if calid in [13, 68]:
        # Output Type: date
        match = re.search(r"^(0?[1-9]|1[0-2])\/(0?[1-9]|[12][0-9]|3[01])\/(\d{4})", raw_answer)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            year = match.group(3)
            answer = f"{month:02}/{day:02}/{year}"
        else:
            answer = "N/A"
        if answer == ground_truth:
            correctness = 1
        else:
            correctness = 0
    elif calid in [69]:
        # Output Type: integer (A, B)
        match = re.search(r"\(?[\"\']?(\d+)\s*(weeks?)?[\"\']?,?\s*[\"\']?(\d+)\s*(days?)?[\"\']?\s*\)?", ground_truth)
        ground_truth = f"({match.group(1)}, {match.group(3)})"
        raw_answer = raw_answer.replace("[", "(").replace("]", ")").replace("'", "").replace('"', "")
        match = re.search(r"\(?[\"\']?(\d+)\s*(weeks?)?[\"\']?,?\s*[\"\']?(\d+)\s*(days?)?[\"\']?\s*\)?", raw_answer)
        if match:
            weeks = match.group(1)
            days = match.group(3)
            answer = f"({weeks}, {days})"
            if eval(answer) == eval(ground_truth):
                correctness = 1
            else:
                correctness = 0
        else:
            answer = "N/A"
            correctness = 0
    elif calid in [4, 15, 16, 17, 18, 20, 21, 25, 27, 28, 29, 32, 33, 36, 43, 45, 48, 51, 69]:
        # Output Type: integer A
        match = re.search(r"(\d+) out of", raw_answer)
        if match: # cases like "3 out of 5"
            answer = match.group(1)
        else:
            match = re.search(r"-?\d+(, ?-?\d+)+", raw_answer)
            if match: # cases like "3, 4, 5"
                answer = str(len(match.group(0).split(",")))
            else:
                # match = re.findall(r"(?<!-)\d+", raw_answer)
                match = re.findall(r"(-?\d+(\.\d+)?)", raw_answer)
                # match = re.findall(r"-?\d+", raw_answer)
                if len(match) > 0: # find the last integer
                    answer = match[-1][0]
                    # answer = match[-1].lstrip("0")
                else:
                    answer = "N/A"
        if answer == "N/A":
            correctness = 0
        elif round(eval(answer)) == eval(ground_truth):
            correctness = 1
        else:
            correctness = 0
    elif calid in [2,  3,  5,  6,  7,  8,  9, 10, 11, 19, 22, 23, 24, 26, 30, 31, 38, 39, 40, 44, 46, 49, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]:
        # Output Type: decimal
        match = re.search(r"str\((.*)\)", raw_answer)
        if match: # cases like "str(round((140 * (3.15 - 136) / 1400) * 72.36)"
            expression = match.group(1).replace("^", "**").replace("is odd", "% 2 == 1").replace("is even", "% 2 == 0").replace("sqrt", "math.sqrt").replace(".math", "").replace("weight", "").replace("height", "").replace("mg/dl", "").replace("g/dl", "").replace("mmol/L", "").replace("kg", "").replace("g", "").replace("mEq/L", "")
            expression = expression.split('#')[0] # cases like round(45.5 * 166 - 45.3 + 0.4 * (75 - (45.5 * 166 - 45.3))))) # Calculation: ...
            if expression.count('(') > expression.count(')'): # add missing ')
                expression += ')' * (expression.count('(') - expression.count(')'))
            elif expression.count(')') > expression.count('('): # add missing (
                expression = '(' * (expression.count(')') - expression.count('(')) + expression
            try:
                answer = eval(expression, {"__builtins__": None}, {"min": min, "pow": pow, "round": round, "abs": abs, "int": int, "float": float, "math": math, "np": np, "numpy": np})
            except:
                print(f"Error in evaluating expression: {expression}")
                answer = "N/A"
        else:
            match = re.search(r"(-?\d+(\.\d+)?)\s*mL/min/1.73", raw_answer)
            if match: # cases like "8.1 mL/min/1.73 m\u00b2"
                answer = eval(match.group(1))
            else:
                match = re.findall(r"(-?\d+(\.\d+)?)\%", raw_answer)
                if len(match) > 0: # cases like "53.1%"
                    answer = eval(match[-1][0]) / 100
                    # answer = eval(match[-1][0].lstrip("0") if len(match[-1][0]) > 1 else match[-1][0]) / 100
                else:
                    match = re.findall(r"(-?\d+(\.\d+)?)", raw_answer)
                    if len(match) > 0: # cases like "8.1 mL/min/1.73 m\u00b2" or "11.1"
                        answer = eval(match[-1][0])
                        # answer = eval(match[-1][0].lstrip("0") if len(match[-1][0]) > 1 else match[-1][0])
                    else:
                        answer = "N/A"
        if answer == "N/A":
            correctness = 0
        elif answer >= eval(lower_limit) and answer <= eval(upper_limit):
            answer = str(answer)
            correctness = 1
        else:
            answer = str(answer)
            correctness = 0
    else:
        raise ValueError(f"Unknown calculator ID: {calid}")
    return answer, str(correctness)

def zero_shot(note, question):

    system_msg = 'You are a helpful assistant for calculating a score for a given patient note. Please think step-by-step to solve the question and then generate the required score. Your output should only contain a JSON dict formatted as {"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}.'

    user_temp = f'Here is the patient note:\n{note}\n\nHere is the task:\n{question}\n\nPlease directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}:'

    return system_msg, user_temp
   

def direct_answer(note, question):

    system_msg = 'You are a helpful assistant for calculating a score for a given patient note. Please output answer only without any other text. Your output should only contain a JSON dict formatted as {"answer": str(value which is the answer to the question)}.'

    user_temp = f'Here is the patient note:\n{note}\n\nHere is the task:\n{question}\n\nPlease directly output the JSON dict formatted as {{"answer": str(value which is the answer to the question)}}:'

    return system_msg, user_temp


def one_shot(note, question, example_note, example_output):

    system_msg = 'You are a helpful assistant for calculating a score for a given patient note. Please think step-by-step to solve the question and then generate the required score. Your output should only contain a JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}.'
    system_msg += f'Here is an example patient note:\n\n{example_note}'
    system_msg += f'\n\nHere is an example task:\n\n{question}'
    system_msg += f'\n\nPlease directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(value which is the answer to the question)}}:\n\n{json.dumps(example_output)}'
    
    user_temp = f'Here is the patient note:\n{note}\n\nHere is the task:\n{question}\n\n. Please directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}:'
    
    return system_msg, user_temp



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument('--model', type=str, help='Specify which model you are using. Options are mistral_7b, mixtral_8x7b, llama3_8b, llama3_70b, meditron_70b')
    parser.add_argument('--response_setting', type=str, help='Specify prompt type. Options are one_shot, zero_shot, direct_answer')

    args = parser.parse_args()

    model_name = args.model
    prompt_style = args.response_setting

    output_path = f"{prompt_style}_{model_name}.json"

    df = pd.read_csv("/Users/khandekarns/Documents/MedCalc-Bench-Internal/ground_truth_data.csv")

    with open("/Users/khandekarns/Documents/MedCalc-Bench-Internal/one_shot_finalized_explanations.json") as file:
        one_shot_json = json.load(file)

    
    responses = {
        "Row Number": [],  
        "Calculator Name": [],
        "Note ID": [],
        "Patient Note": [],
        "Question": [], 
        "LLM Answer": [],
        "LLM Explanation": [],
        "Ground Answer": [],
        "Ground Truth Explanation": [],  
        "Result": []
    }


    for index, row in df.iterrows():


        patient_note = row["Patient Note"]
        question = row["Question"] 
        calculator_id = str(row["Calculator ID"])
        calculator_name = str(row["Calculator Name"])
        note_id = str(row["Note ID"])
        ground_truth_answer = row["Ground Truth Answer"]


        if prompt_style == "zero_shot":
            system, user = zero_shot(patient_note, question)

        elif prompt_style == "one_shot" and calculator_id in one_shot_json:
            # system, user = one_shot(patient_note, question, one_shot_json[calculator_id]["explanation"], example)
            example = one_shot_json[calculator_id]
            system, user = one_shot(patient_note, question, example["Patient Note"], {"step_by_step_thinking": example["Response"]["step_by_step_thinking"], "answer": example["Response"]["answer"]["Answer"]})

        elif prompt_style == "direct_answer":
            system, user = direct_answer(patient_note, question)


        response = client.chat.completions.create(
            model=model_name,
            messages=   [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,
        )

        output = response.choices[0].message

        responses["Row Number"].append(str(index + 1))
        responses["Calculator Name"].append(calculator_name)
        responses["Note ID"].append(note_id)
        responses["Patient Note"].append(patient_note)
        responses["Question"].append(question)

        responses["LLM Answer"].append()
        responses["LLM Explanation"].append(question)
        responses["Ground Truth Answer"].append(ground_truth_answer)


        

    with open(output_path, "w") as file:
        json.dump(responses, file, indent=4)



    