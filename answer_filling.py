from utils.model import get_structured_llm
from utils.utils import Response, ModelConfig 
from utils.prompt import answer_filling_instruction, create_chat_prompt
from utils.utils import get_data_from_json
from tqdm import tqdm
import pandas as pd


def answer_filling(whole_path: str, save_path: str, batch_size: int = 10) -> None:
    config = ModelConfig()
    # 답변시 parsing error가 발생할 경우를 대비할수 있도록 include_raw=True로 설정
    answerer = get_structured_llm(Response, config=config, include_raw=True)
    
    prompt = create_chat_prompt()
    answering_chain = prompt | answerer

    # 데이터 준비
    temp_df = pd.DataFrame(get_data_from_json(whole_path))
    temp_dict = temp_df.loc[temp_df['output'] == 'IDK', ['instruction']].to_dict('list')
    
    questions = temp_dict['instruction']
    population = len(questions)
    
    print("답변을 채워야할 instruction 수:",len(temp_df.loc[temp_df['output'] == 'IDK']))
    print("답변이 이미 존재하는 instruction 수:",len(temp_df.loc[temp_df['output'] != 'IDK']))
    
    responses = []
    for idx in tqdm(range(0, population, batch_size)):
        start, end = idx, idx + batch_size if idx + batch_size < population else None

        batch_questions = questions[start:end]
        batch_questions = [answer_filling_instruction.format(question=q) for q in batch_questions]
        # batch inference
        batch_responses = answering_chain.batch(batch_questions) # bs=5 -> 40초 bs=10 -> 70초
        temp = []
        for res in batch_responses:
            if res['parsing_error']:
                # json_error = res['raw'].additional_kwargs['tool_calls'][0]['function']['arguments']
                temp.append("parsing_error")
            else:
                temp.append(res['parsed'].answer)
        responses += temp
        
    temp_df.loc[temp_df['output'] == 'IDK', ['output']] = responses
    temp_df.to_json(path_or_buf=save_path, orient='split', index=False)