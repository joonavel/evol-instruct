import pandas as pd
from typing import Dict, List
from pydantic import BaseModel, Field
import random


# Pydantic
class RewrittenPrompt(BaseModel):
    """Rewritten Prompt to give to user."""

    prompt: str = Field(description="Rewritten prompt from the given prompt")

class EqualityResult(BaseModel):
    """Result of equality of the first prompt and the second prompt."""

    result: int = Field(description="1 for Equal or 0 for Not Equal")
    
class Response(BaseModel):
    """Answer to the user."""

    answer: str = Field(description="Answer from the given question. If you don't know answer, answer with IDK.")

class ModelConfig(BaseModel):
    temperature: float = 1.0
    top_p: float = 0.9
    max_tokens: int = 2048
    timeout: int = 100
    max_retries: int = 2

# seed
def set_seed(seed: int = 42):
    random.seed(seed)

def get_data_from_json(file_path: str = './seed_instruction.json', test_run: bool = False) -> Dict[str, List]:
    '''데이터를 Dict[str, List] 형태로 만들어 반환하는 함수입니다.
    file_path의 확장자는 반드시 .json이어야 합니다.

    file_path: .json 확장자로 저장된 seed 데이터'''
    # instruction, generation, root, trace, origin
    if test_run:
        data = pd.read_json(file_path, orient='split', dtype={'trace':'str'})[:10].to_dict('list')
    else:
        data = pd.read_json(file_path, orient='split', dtype={'trace':'str'}).to_dict('list')
    print(f"data's keys: {data.keys()}")
    return data


def check_failure(before, after):
    if before == after:
        return False #, "same"
    if after.count('\n') > after.count(" ") * 2:
        return False #, "too many lines"
    if "#Rewritten Prompt#" in after:
        return False #, "prompt leaked 1"
    if "rewritten prompt" in after.lower():
        return False #, "prompt leaked 2"
    if "openai" in after.lower():
        return False #, "AI"
    if "deepseek" in after.lower():
        return False #, "AI"
    if "gpt" in after.lower() and "gpt" not in before.lower():
        return False #, "AI"
    if "죄송하지만" in after.lower() and "죄송" not in before.lower() and len(after) < len(before):
        return False #, "sorry"
    if "�" in after and not "�" in before:
        return False #, "replacement character"
    return True #, ""

def check_flag_true(array, flags):
    return [x for x, flag in zip(array, flags) if flag]

def check_flag_false(array, flags):
    return [x for x, flag in zip(array, flags) if not flag]

def make_empty_structure():
    return {
            "instruction":[],
            "generation":[],
            "root":[],
            "trace":[],
            "origin":[],
            }
    
def make_empty_structure_for_failures():
    return {
        "parent": [],
        "child": [],
        "generation": [],
        "root": [],
        "trace": [],
        "origin": [],
    }
