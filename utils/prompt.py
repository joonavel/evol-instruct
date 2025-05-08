from langchain_core.prompts import ChatPromptTemplate


def create_chat_prompt(system_prompt: str = "") -> ChatPromptTemplate:
    """
    system_prompt: str - 시스템 프롬프트
    """
    if not system_prompt:
        system_prompt = "You are a helpful assistant."

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                system_prompt,
            ),
            ("human", "{input}"),
        ]
    )
    return prompt