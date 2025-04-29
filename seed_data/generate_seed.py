from datasets import load_dataset, get_dataset_config_names
import pandas as pd
import re
from typing import List, Dict


def load_datasets(repo_names: List[str]) -> Dict[str, List]:
    dataset_dict = {
        'with_subset': [],
        'without_subset': [],
    }
    
    for repo_name in repo_names:
        # subset 확인 subset이 없으면 'default'만 존재
        subset_names = get_dataset_config_names(repo_name)
        
        if len(subset_names) > 1:  # subset이 있는 경우
            temp_dict = {name: load_dataset(repo_name, name, split="train") for name in subset_names}
            dataset_dict['with_subset'].append({f"{repo_name}": [temp_dict, subset_names]})
            
        else:  # subset이 없는 경우
            dataset = load_dataset(repo_name, split="train")
            dataset_dict['without_subset'].append({f"{repo_name}": dataset})
        
        print(f"{repo_name} 데이터셋 불러오기 완료")
    
    return dataset_dict


def do_sampling(dataset_dict: Dict[str, List], seed: int=42, subset_ext_cnt: int=10, ext_cnt: int=100):
    raw_list = []
    raw_sources = []
    
    for ds_dict in dataset_dict['with_subset']:
        for repo_name in ds_dict.keys():
            subset_dict, subset_names = ds_dict[repo_name]
            for subset_name in subset_names:
                temp_dataset = subset_dict[subset_name]
                if len(temp_dataset) < 5:
                    raw_list += temp_dataset['question']
                    raw_sources += [f'{repo_name}/{subset_name}'] * len(temp_dataset)
                else:
                    raw_list += temp_dataset.shuffle(seed=seed).select(range(subset_ext_cnt))['question']
                    raw_sources += [f'{repo_name}/{subset_name}'] * subset_ext_cnt
                    

    for ds_dict in dataset_dict['without_subset']:
        for repo_name in ds_dict.keys():
            temp_dataset = ds_dict[repo_name].shuffle(seed=seed).select(range(ext_cnt))
            raw_list += temp_dataset['instruction']
            raw_sources += [f'{repo_name}'] * ext_cnt
    
    raw_df = pd.DataFrame(
        {"instruction":raw_list,
        "generation":[0 for _ in range(len(raw_list))],
        "root": raw_sources,
        "trace": ["r" for _ in range(len(raw_list))],
        "origin": raw_list,
        })
    
    return raw_df

def preprocess(raw_df: pd.DataFrame) -> pd.DataFrame:
    deny_patterns = [
    "옳지 않은 것은?",
    "아닌 것은?",
    "않는 것은?",
    "잘못된 것은?",
    "것으로 옳은 것은?",
    "옳은 것은?",
    "내용으로 틀린 것은?",
    "설명으로 틀린 것은?",
    "틀린 것은?",
    "관계 없는 것은?",
    "관련이 없는 것은?",
    "먼 것은?",
    "볼수 없는 것은?",
    "설명한 것은?",
    "해당하는 것은?",
    "에러(error) 정정이 가능한 코드는?",
    "강점관점에 관한 설명으로 옳지 않은 것은",
    ]
    pattern = '|'.join(map(re.escape, deny_patterns))
    
    filtered_df = raw_df[~raw_df['instruction'].str.contains(pattern)]
    filtered_df.reset_index(drop=True, inplace=True)
    
    return filtered_df

def export(filtered_df: pd.DataFrame, save_path: str="../seed_instruction.json"):
    filtered_df.to_json(path_or_buf=save_path, orient='split', index=False)


def generate_seed(repo_names: List[str], seed: int=42, subset_ext_cnt: int=10, ext_cnt: int=100, save_path: str="../seed_instruction.json"):
    # 데이터셋 불러오기
    print("데이터셋 불러오기 시작")
    dataset_dict = load_datasets(repo_names)
    print("데이터셋 불러오기 완료")
    # 샘플링
    raw_df = do_sampling(dataset_dict, seed, subset_ext_cnt, ext_cnt)
    print("샘플링 완료")
    # 전처리
    filtered_df = preprocess(raw_df)
    print("전처리 완료")
    # export
    export(filtered_df, save_path)
    print("export 완료")
    print(f"저장 경로: {save_path}")
    return