__author__ = "guangzhi"
'''
Adapted from https://github.com/Teddy-XiongGZ/MedRAG/blob/main/src/medrag.py
'''

import os
import re
import json
import tqdm
import torch
import time
import argparse
import transformers
from transformers import AutoTokenizer
import openai
from transformers import StoppingCriteria, StoppingCriteriaList
import tiktoken
import openai
import sys
import google.generativeai as genai


class ExecuteLLM:

    def __init__(self, llm_name="OpenAI/gpt-3.5-turbo", cache_dir="../../huggingface/hub"):
        self.llm_name = llm_name
        self.cache_dir = cache_dir
        if self.llm_name.split('/')[0].lower() == "openai":
            self.model = self.llm_name.split('/')[-1]
            if "gpt-3.5" in self.model or "gpt-35" in self.model:
                self.max_length = 16384
            elif "gpt-4" in self.model:
                self.max_length = 32768
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
            self.client = openai.AzureOpenAI(
                api_version="2024-03-01-preview",
                azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        elif "gemini" in self.llm_name.lower():
            genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
            self.model = genai.GenerativeModel(
                model_name=self.llm_name,
                generation_config={
                    "temperature": 0,
                    "max_output_tokens": 2048,
                }
            )
            if "1.5" in self.llm_name.lower():
                self.max_length = 1048576
            else:
                self.max_length = 30720
            self.tokenizer = tiktoken.get_encoding("cl100k_base")            
        else:
            self.type = torch.bfloat16
            self.tokenizer = AutoTokenizer.from_pretrained(self.llm_name, cache_dir=self.cache_dir)
            if "mixtral" in llm_name.lower() or "mistral" in llm_name.lower():
                self.tokenizer.chat_template = open('./templates/mistral-instruct.jinja').read().replace('    ', '').replace('\n', '')
                self.max_length = 32768
            elif "llama-2" in llm_name.lower():
                self.max_length = 4096
                self.type = torch.float16
            elif "llama-3" in llm_name.lower():
                self.max_length = 8192
            elif "meditron-70b" in llm_name.lower():
                self.tokenizer.chat_template = open('./templates/meditron.jinja').read().replace('    ', '').replace('\n', '')
                self.max_length = 4096
            elif "pmc_llama" in llm_name.lower():
                self.tokenizer.chat_template = open('./templates/pmc_llama.jinja').read().replace('    ', '').replace('\n', '')
                self.max_length = 2048
            elif "command-r" in llm_name.lower():
                self.max_length = 131072
            self.model = transformers.pipeline(
                "text-generation",
                model=self.llm_name,
                torch_dtype=self.type,
                device_map="auto",
                model_kwargs={"cache_dir":self.cache_dir},
            )

    def answer(self, messages):
        # generate answers

        ans = self.generate(messages)
        ans = re.sub("\s+", " ", ans)
        
        return ans

    def custom_stop(self, stop_str, input_len=0):
        stopping_criteria = StoppingCriteriaList([CustomStoppingCriteria(stop_str, self.tokenizer, input_len)])
        return stopping_criteria

    def generate(self, messages, prompt=None):
        '''
        generate response given messages
        '''
        if "openai" in self.llm_name.lower():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
            )
            ans = response.choices[0].message.content

        elif "gemini" in self.llm_name.lower():
            response = self.model.generate_content(messages[0]["content"] + '\n\n' + messages[1]["content"])
            ans = response.candidates[0].content.parts[0].text
        else:
            stopping_criteria = None
            if prompt is None:
                prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            if "meditron" in self.llm_name.lower():
                stopping_criteria = self.custom_stop(["###", "User:", "\n\n\n"], input_len=len(self.tokenizer.encode(prompt, add_special_tokens=True)))
            if "llama-3" in self.llm_name.lower():
                response = self.model(
                    prompt,
                    do_sample=False,
                    eos_token_id=[self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")],
                    pad_token_id=self.tokenizer.eos_token_id,
                    max_length=min(self.max_length, len(self.tokenizer.encode(prompt, add_special_tokens=True)) + 4096),
                    truncation=True,
                    stopping_criteria=stopping_criteria,
                    temperature=0.0
                )
            else:
                response = self.model(
                    prompt,
                    do_sample=False,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.eos_token_id,
                    max_length=min(self.max_length, len(self.tokenizer.encode(prompt, add_special_tokens=True)) + 4096),
                    truncation=True,
                    stopping_criteria=stopping_criteria,
                    temperature=0.0
                )
            ans = response[0]["generated_text"]
        return ans

class CustomStoppingCriteria(StoppingCriteria):
    def __init__(self, stop_words, tokenizer, input_len=0):
        super().__init__()
        self.tokenizer = tokenizer
        self.stops_words = stop_words
        self.input_len = input_len

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        tokens = self.tokenizer.decode(input_ids[0][self.input_len:])
        return any(stop in tokens for stop in self.stops_words)    