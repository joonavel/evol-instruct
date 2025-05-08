from langchain_deepseek import ChatDeepSeek
from utils import ModelConfig

def get_structured_llm(basemodel, model_name: str = "deepseek-chat", config: ModelConfig | None = None, **kwargs):
    '''LangChain의 프레임 워크를 이용해서 구조화된 출력을 반환하는 ChatDeepSeek 모델을 반환하는 함수입니다.
    basemodel: 출력 구조를 정의하는 langchain_core.pydantic_v1.BaseModel
    model_name: str = "deepseek-chat"
    config: ModelConfig - temperature, top_p, max_tokens, timeout, max_retries 등을 포함하는 langchain_core.pydantic_v1.BaseModel
    kwargs: dict - ModelConfig 이외에 특별한 설정을 위해 사용되는는 인자들
    '''
    if config is None:
        config = ModelConfig()
    
    # 기본 설정과 추가 설정을 병합
    model_params = config.model_dump()
    model_params.update(kwargs)
    
    llm = ChatDeepSeek(
        model=model_name,
        **model_params
    )

    structured_llm = llm.with_structured_output(basemodel)
    return structured_llm