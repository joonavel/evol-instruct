from utils.model import get_structured_llm
from utils.utils import RewrittenPrompt, EqualityResult, set_seed, ModelConfig
from utils.prompt import create_chat_prompt
import random, os, getpass
from dotenv import load_dotenv
from make_prompt import (createBreadthPrompt, createComplicatingPrompt, createConcretizingPrompt,
                         createConstraintsPrompt, createDeepenPrompt, createReasoningPrompt,
                         equality_check_instruction)
from utils.utils import get_data_from_json, make_empty_structure, make_empty_structure_for_failures, check_failure, check_flag_true, check_flag_false
from tqdm import tqdm
import pandas as pd

use_local = False
use_deepseek = True

load_dotenv()
if not use_local and use_deepseek:
    if not os.getenv("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")
    
def mutate(current_generations, failures, templates, batch_size, mutation_chain, validation_chain):
    population = len(current_generations['generation'])
    template_ids = [k for k in range(len(templates))]
    next_generations = make_empty_structure()

    for idx in tqdm(range(0, population, batch_size)):
        start, end = idx, idx + batch_size if idx + batch_size < population else None

        # slicing by batch
        temp_dict = make_empty_structure()
        for key in temp_dict.keys():
            if key == "generation":
                temp_dict[key] = [x+1 for x in current_generations[key][start:end]]
            else:
                temp_dict[key] = current_generations[key][start:end]

        # mutation template 중 무작위 택1
        chosen_templates = [random.choice(template_ids) for _ in temp_dict['generation']]
        traces = []
        for trace, template_idx in zip(temp_dict['trace'], chosen_templates):
            temp = trace + str(template_idx) if trace is not None else str(template_idx)
            traces.append(temp)
        temp_dict['trace'] = traces

        # 배치 데이터에 template을 적용
        batch_input = [templates[i](seed) for i, seed in zip(chosen_templates, temp_dict["instruction"])]
        # batch inference
        batch_responses = mutation_chain.batch(batch_input) # bs=5 -> 40초 bs=10 -> 70초
        # 필요한 답변 추출
        candidates = [response.prompt for response in batch_responses]

        # 답변 후처리
        flags = [check_failure(seed, candidate) for seed, candidate in zip(temp_dict["instruction"], candidates)]
        # 후처리 결과에 따라 추출
        candidates = check_flag_true(candidates, flags)
        for key in temp_dict.keys():
            temp_dict[key] = check_flag_true(temp_dict[key], flags)

        # validation을 위해 template 적용
        batch_val_input = [equality_check_instruction.format(parent=parent, child=child) for parent, child in zip(temp_dict["instruction"], candidates)]
        # batch inference
        batch_val = validation_chain.batch(batch_val_input)
        # validation 결과 추출
        results = [val.result for val in batch_val]

        # validation(equality check)을 통과하지 못한 결과들 저장
        failures['parent'] += check_flag_true(temp_dict['instruction'], results)
        failures['child'] += check_flag_true(candidates, results)

        # validation을 통과한 데이터만 다음 세대로
        candidates = check_flag_false(candidates, results)
        next_generations['instruction'] += candidates

        for key in temp_dict.keys():
            if key == "instruction":
                continue
            next_generations[key] += check_flag_false(temp_dict[key], results)
            failures[key] += check_flag_true(temp_dict[key], results)
            
    return next_generations, failures


def evolve(seed_path: str, whole_path: str, failures_path: str, total_gen: int, batch_size: int,
           seed: int = 42, save_location: str = "./", save_last_gen: bool = False, test_run: bool = False) -> None:
    set_seed(seed)
    
    # 모델 준비
    mutator = get_structured_llm(RewrittenPrompt) # 기본 config 사용

    validator_config = ModelConfig(temperature=0,max_tokens=100,timeout=100,max_retries=2)
    validator = get_structured_llm(EqualityResult, config=validator_config)
    # 프롬프트 준비
    prompt = create_chat_prompt()
    # 체인 생성
    mutation_chain = prompt | mutator
    validation_chain = prompt | validator

    # evolution을 위한 데이터 준비
    current_generations = get_data_from_json(seed_path, test_run)
    whole_generations = get_data_from_json(whole_path) if whole_path else get_data_from_json(seed_path, test_run)
    failures = get_data_from_json(failures_path) if failures_path else make_empty_structure_for_failures()
    
    templates = [createBreadthPrompt, createComplicatingPrompt, createConcretizingPrompt,
                createConstraintsPrompt, createDeepenPrompt, createReasoningPrompt]
    
    for _ in range(total_gen):
        next_generations, failures = mutate(current_generations, failures, templates, batch_size, mutation_chain, validation_chain)

        for key in next_generations.keys():
            whole_generations[key] += next_generations[key]

        current_generations = next_generations
    
    # 최종 결과 저장
    pd.DataFrame(whole_generations).to_json(path_or_buf=save_location+"whole_generations.json",
                                            orient='split', index=False)
    pd.DataFrame(failures).to_json(path_or_buf=save_location+"failures.json",
                                  orient='split', index=False)
    if save_last_gen:
        pd.DataFrame(current_generations).to_json(path_or_buf=save_location+f"gen_{total_gen}.json",
                                                  orient='split', index=False)
        
evolve(seed_path='./seed_instruction.json', whole_path='', failures_path='',
       total_gen=5, batch_size=5, save_location='./', save_last_gen=True, test_run=True)