import json
import os
import sys
import pandas as pd
from importlib.machinery import SourceFileLoader

from langchain.tools import StructuredTool

RESOURCE_NAMES = []
CALCULATOR_DIR = "/Users/caravanuden/git-repos/qualified-health/qh-agent/src/calculators/"
CALCULATOR_METADATA_PATH = os.path.join(CALCULATOR_DIR, "processed_metadata.json")
CALCULATOR_EXAMPLES_PATH = os.path.join(CALCULATOR_DIR, "dataset/test_data.csv")
CALCULATOR_IMPL_DIR = os.path.join(CALCULATOR_DIR, "calculator_implementations")

NUM_EXAMPLES = 1

sys.path.append(CALCULATOR_IMPL_DIR)

# desc = f"""Calculator for {calculator_name}. Returns both the answer and a step-by-step explanation of how the answer was calculated.

# Args:
#     input (Dict[str, Any]): A dict with the keys: {data[calculator_name]['method_input_params']}.
    
# Returns:
#     Dict[str, Any]: A dict with the keys: ['Explanation', 'Answer'].

# Example Inputs/Outputs:
# {examples_for_calculator}
# """

def create_tools_calculators(calculator_metadata_path=CALCULATOR_METADATA_PATH):
    with open(calculator_metadata_path) as file:
        data = json.load(file)

    examples = pd.read_csv(CALCULATOR_EXAMPLES_PATH)
    tools = []
    for calculator_name in data.keys():
        module_path = os.path.join(CALCULATOR_DIR, data[calculator_name]['file_path'])
        module_name = module_path.split("/")[-1]

        module = SourceFileLoader(module_name, module_path).load_module()
        method = getattr(module, data[calculator_name]['method_name'])

        examples_for_calculator_df = examples[examples['Calculator ID'] == data[calculator_name]['calculator_id']]
        examples_for_calculator_df = examples_for_calculator_df.head(NUM_EXAMPLES)

        examples_for_calculator = []
        for i, row in examples_for_calculator_df.iterrows():
            example_for_calculator = {}
            example_for_calculator['input'] = row['Relevant Entities']
            example_for_calculator['output'] = {'Explanation': 'EXPLANATION HERE', 'Answer': row['Ground Truth Answer']}

            examples_for_calculator.append(example_for_calculator)

        desc = f"""Calculator for {calculator_name}. Returns both the answer and a step-by-step explanation of how the answer was calculated.

Example Inputs/Outputs:
{examples_for_calculator}
"""
        tool = StructuredTool.from_function(
            func=lambda kwargs: method(kwargs),
            name=f"calculator-{data[calculator_name]['method_name']}",
            description=desc,
            return_direct=False, # note that we can't have `True` in an AgentExecutor
            # coroutine= ... <- you can specify an async method if desired as well
        )

        tools.append(tool)

    return tools