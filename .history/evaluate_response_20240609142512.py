import json
import os
from openai import AzureOpenAI
import argparse
import pandas as pd

client = AzureOpenAI(
	api_version="2024-03-01-preview",
	azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
	api_key=os.getenv("OPENAI_API_KEY"),
)

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

    with open("/Users/khandekarns/Documents/MedCalc-Bench-Internal/one_shot_explanations.json") as file:
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


        responses["LLM Answer"].append(question)
        responses["LLM Explanation"].append(question)

        responses["Ground Truth Answer"].append("Ground Truth Answer")
        

        

    with open(output_path, "w") as file:
        json.dump(one_shot_json, file, indent=4)



    