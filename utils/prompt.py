from langchain_core.prompts import ChatPromptTemplate
import os

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

def read_prompt_file(filename):
    with open(os.path.join('prompts', filename), 'r', encoding='utf-8') as f:
        content = f.read()
        return content.replace('\\r\\n', '\n').replace('\\n', '\n')

depth_instruction = read_prompt_file('depth_instruction.prompt')
breadth_instruction = read_prompt_file('breadth_instruction.prompt')
equality_check_instruction = read_prompt_file('equality_check_instruction.prompt')
answer_filling_instruction = read_prompt_file('answer_filling_instruction.prompt')

def createConstraintsPrompt(instruction):
    prompt = depth_instruction.format("Please add one more constraints/requirements into #The Given Prompt#'")
    prompt += "Write in Korean.\n"
    prompt += "#The Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt

def createDeepenPrompt(instruction):
    prompt = depth_instruction.format("If #The Given Prompt# contains inquiries about certain issues, the depth and breadth of the inquiry can be increased.")
    prompt += "Write in Korean.\n"
    prompt += "#The Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt

def createConcretizingPrompt(instruction):
    prompt = depth_instruction.format("Please replace general concepts with more specific concepts.")
    prompt += "Write in Korean."
    prompt += "#The Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt


def createReasoningPrompt(instruction):
    prompt = depth_instruction.format("If #The Given Prompt# can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.")
    prompt += "Write in Korean."
    prompt += "#The Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt

def createComplicatingPrompt(instruction):
    prompt = depth_instruction.format("Rewrite #Given Prompt# to make it slightly more complicated.")
    prompt += "Write in Korean."
    prompt += "#The Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt

def createBreadthPrompt(instruction):
    prompt = breadth_instruction
    prompt += "Write in Korean."
    prompt += "#Given Prompt#: \r\n {} \r\n".format(instruction)
    return prompt