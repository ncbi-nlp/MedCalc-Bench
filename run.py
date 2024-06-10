import re
import os
import json
import tqdm
import argparse
import pandas as pd
import sys
from execute_llm import ExecuteLLM
from evaluate import check_correctness

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

def zero_shot_meditron(note, question):
    system_msg = '''You are a helpful assistant for calculating a score for a given patient note. Please think step-by-step to solve the question and then generate the required score. Your output should only contain a JSON dict formatted as {"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}. Here is a demonstration (Replace the rationale and "X.XX" with your actual rationale and calculated value):\n\n### User:\nHere is the patient note:\n...\n\nHere is the task:\n...?\n\nPlease directly output the JSON dict formatted as {"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}.\n\n### Assistant:\n{"step_by_step_thinking": rationale, "answer": X.XX}'''
    user_temp = f'### User:\nHere is the patient note:\n{note}\n\nHere is the task:\n{question}\n\nPlease directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}.\n\n### Assistant:\n'
    return system_msg, user_temp
   
def direct_answer_meditron(note, question):
    system_msg = 'You are a helpful assistant for calculating a score for a given patient note. Please output answer only without any other text. Your output should only contain a JSON dict formatted as {"answer": str(value which is the answer to the question)}. Here is a demonstration (Replace "X.XX" with your the actual calculated value):\n\n### User:\nHere is the patient note:\n...\n\nHere is the task:\n...?\n\nPlease directly output the JSON dict formatted as {"answer": str(value which is the answer to the question)}.\n\n### Assistant:\n{"answer": X.XX}'
    user_temp = f'### User:\nHere is the patient note:\n{note}\n\nHere is the task:\n{question}\n\nPlease directly output the JSON dict formatted as {{"answer": str(value which is the answer to the question)}}.\n\n### Assistant:\n'
    return system_msg, user_temp

def one_shot_meditron(note, question, example_note, example_output):
    system_msg = 'You are a helpful assistant for calculating a score for a given patient note. Please think step-by-step to solve the question and then generate the required score. Your output should only contain a JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}.'
    system_msg += f'\n\n### User:\nHere is an example patient note:\n{example_note}'
    system_msg += f'\n\nHere is an example task:\n{question}'
    system_msg += f'\n\nPlease directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(value which is the answer to the question)}}:\n\n### Assistant:\n{json.dumps(example_output)}'
    user_temp = f'### User:\nHere is the patient note:\n{note}\n\nHere is the task:\n{question}\n\n. Please directly output the JSON dict formatted as {{"step_by_step_thinking": str(your_step_by_step_thinking_procress_to_solve_the_question), "answer": str(short_and_direct_answer_of_the_question)}}:\n\n### Assistant:\n'
    return system_msg, user_temp

def extract_answer(answer, calid):
    extracted_answer = re.findall(r'[Aa]nswer":\s*(.*?)\}', answer)
    if len(extracted_answer) == 0:
        extracted_answer = "not found"
    else:
        extracted_answer = extracted_answer[-1].strip().strip('"')
        if extracted_answer == "str(short_and_direct_answer_of_the_question)" or extracted_answer == "str(value which is the answer to the question)" or extracted_answer == "X.XX":
            extracted_answer = "not found"
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
        else:
            answer = "N/A"
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
                else:
                    match = re.findall(r"(-?\d+(\.\d+)?)", raw_answer)
                    if len(match) > 0: # cases like "8.1 mL/min/1.73 m\u00b2" or "11.1"
                        answer = eval(match[-1][0])
                    else:
                        answer = "N/A"
        if answer != "N/A":
            answer = str(answer)           
    return extracted_answer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument('--model', type=str, help='Specify which model you are using. Options are mistralai/Mistral-7B-Instruct-v0.2, mistralai/Mixtral-8x7B-Instruct-v0.1, meta-llama/Meta-Llama-3-8B-Instruct, meta-llama/Meta-Llama-3-70B-Instruct, epfl-llm/meditron-70b, axiong/PMC_LLaMA_13B')
    parser.add_argument('--prompt', type=str, help='Specify prompt type. Options are one_shot, zero_shot, direct_answer')
    parser.add_argument('--ground_truth_path', type=str, default="../data/ground_truth_data.csv", help='Path to ground truth data')
    parser.add_argument('--one_shot_example_path', type=str, default="../one_shot_finalized_explanation.json", help='Path to one shot example data')

    args = parser.parse_args()

    model_name = args.model
    prompt_style = args.prompt

    output_path = f"{prompt_style}_{model_name.replace('/', '_')}.json"

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    if not os.path.exists(os.path.join("outputs", output_path)):
        existing = None
    else:
        existing = pd.read_json(os.path.join("outputs", output_path), lines=True)
        existing["Calculator ID"] = existing["Calculator ID"].astype(str)
        existing["Note ID"] = existing["Note ID"].astype(str)

    if "meditron" in model_name.lower():
        zero_shot = zero_shot_meditron
        direct_answer = direct_answer_meditron
        one_shot = one_shot_meditron

    llm = ExecuteLLM(llm_name=model_name)

    one_shot_json = json.load(open(args.one_shot_example_path))

    df = pd.read_csv(args.ground_truth_path)

    for index in tqdm.tqdm(range(len(df))):

        row = df.iloc[index]

        patient_note = row["Patient Note"]
        question = row["Question"] 
        calculator_id = str(row["Calculator ID"])
        note_id = str(row["Note ID"])

        if existing is not None:
            if existing[(existing["Calculator ID"] == calculator_id) & (existing["Note ID"] == str(row["Note ID"]))].shape[0] > 0:
                continue

        if "pmc_llama" in model_name.lower():
            patient_note = llm.tokenizer.decode(llm.tokenizer.encode(patient_note, add_special_tokens=False)[:256])
        if prompt_style == "zero_shot":
            system, user = zero_shot(patient_note, question)
        elif prompt_style == "one_shot":
            example = one_shot_json[calculator_id]
            if "meditron" in model_name.lower():
                example["Patient Note"] = llm.tokenizer.decode(llm.tokenizer.encode(example["Patient Note"], add_special_tokens=False)[:512])
                example["Response"]["step_by_step_thinking"] = llm.tokenizer.decode(llm.tokenizer.encode(example["Response"]["step_by_step_thinking"], add_special_tokens=False)[:512])
            elif "pmc_llama" in model_name.lower():
                example["Patient Note"] = llm.tokenizer.decode(llm.tokenizer.encode(example["Patient Note"], add_special_tokens=False)[:256])
                example["Response"]["step_by_step_thinking"] = llm.tokenizer.decode(llm.tokenizer.encode(example["Response"]["step_by_step_thinking"], add_special_tokens=False)[:256])
            system, user = one_shot(patient_note, question, example["Patient Note"], {"step_by_step_thinking": example["Response"]["step_by_step_thinking"], "answer": example["Response"]["answer"]})
        elif prompt_style == "direct_answer":
            system, user = direct_answer(patient_note, question)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]

        try:
            answer = llm.answer(messages)

            answer_value = extract_answer(answer, int(calculator_id))

            correctness = check_correctness(answer_value, row["Ground Truth Answer"], calculator_id, row["Upper Limit"], row["Lower Limit"])

            status = "Correct" if correctness else "Incorrect"

            outputs = {
                "Row Number": row["Row Number"],
                "Calculator Name": row["Calculator Name"],
                "Calculator ID": calculator_id,
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": answer_value, 
                "LLM Explanation": answer,
                "Ground Truth Answer": row["Ground Truth Answer"],
                "Ground Truth Explanation": row["Ground Truth Explanation"],
                "Result": status
            }

            if prompt_style == "direct_answer":
                outputs["LLM Explanation"] = "N/A"
        
        except:
            outputs = {
                "Row Number": row["Row Number"],
                "Calculator Name": row["Calculator Name"],
                "Calculator ID": calculator_id,
                "Note ID": note_id,
                "Patient Note": patient_note,
                "Question": question,
                "LLM Answer": "Error", 
                "LLM Explanation": "Error",
                "Ground Truth Answer": row["Ground Truth Answer"],
                "Ground Truth Explanation": row["Ground Truth Explanation"],
                "Result": "Incorrect"
            }
            print(f"error in {calculator_id} {note_id}")
        
        with open(f"outputs/{output_path}", "a") as f:
            f.write(json.dumps(outputs) + "\n")

        # Compute the accuracy of each of the components 
        