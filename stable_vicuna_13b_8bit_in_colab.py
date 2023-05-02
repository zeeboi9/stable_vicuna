# -*- coding: utf-8 -*-
"""Stable_Vicuna_13B_8bit_in_Colab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cttOeIh_7wCrxXRRGJgmcbEIFo8eOT_i
"""

!pip -q install git+https://github.com/huggingface/transformers # need to install from github
!pip install -q datasets loralib sentencepiece 
!pip -q install bitsandbytes accelerate
!pip install flask-ngrok
!nvidia-smi

"""## StableVicuna - RLHF Chat model"""

from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline
import torch


tokenizer = LlamaTokenizer.from_pretrained("TheBloke/stable-vicuna-13B-HF")

base_model = LlamaForCausalLM.from_pretrained(
    "TheBloke/stable-vicuna-13B-HF",
    load_in_8bit=True,
    device_map='auto',
)


pipe = pipeline(
    "text-generation",
    model=base_model, 
    tokenizer=tokenizer, 
    max_length=1024,
    temperature=0.8,
    top_p=0.95,
    repetition_penalty=1.15
)

"""### The prompt & response"""

import json
import textwrap


def get_prompt(human_prompt):
    prompt_template=f"### Human: {human_prompt} \n### Assistant:"
    return prompt_template



def remove_human_text(text):
    return text.split('### Human:', 1)[0]

def parse_text(data):
    for item in data:
        text = item['generated_text']
        assistant_text_index = text.find('### Assistant:')
        if assistant_text_index != -1:
            assistant_text = text[assistant_text_index+len('### Assistant:'):].strip()
            assistant_text = remove_human_text(assistant_text)
            wrapped_text = textwrap.fill(assistant_text, width=100)
            print(wrapped_text)

"""## Run it as a HF model"""

#%%time 
raw_output = pipe(get_prompt('What is the capital of England?'))
#parse_text(raw_output)