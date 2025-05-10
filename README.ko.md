# koevol-instruct

[English](README.md) | [한국어](README.ko.md)

## Introduction
이 레포는 아래 논문의 evol-instruct(evolving)기법을 참고하여 instruction evolution을 통해 한국어 데이터를 증강시키기 위한 자동화 알고리즘을 구현한 레포입니다.

WizardLM: Empowering Large Language Models to Follow Complex Instructions
(https://arxiv.org/abs/2304.12244)

## Installation
```bash
pip install -r requirements.txt
```

## Setting Environment Variables
프로젝트를 실행하기 전에 다음 환경 변수를 .env 파일에 설정해야 합니다:
```
DEEPSEEK_API_KEY=your_deepseek_api_key
MY_HF_TOKEN=your_huggingface_api_key
```

## Project Structure
```
.
├── main.py              # 메인 실행 파일
├── evolving.py          # instruction evolution 로직
├── answer_filling.py    # 생성된 instruction에 대한 답변 생성
├── main.sh             # 실행 스크립트
├── requirements.txt     # 의존성 패키지 목록
├── seed_instruction.json # 초기 seed instruction 데이터
├── prompts/            # 프롬프트 템플릿 디렉토리
├── utils/              # 유틸리티 함수들
└── seed_data/          # 초기 seed instruction 데이터를 직접 만들 수 있는 디렉터리
```

## Usage
사용법은 다음과 같으며, 테스트 실행은 test-run을 1로 실제 실행은 0으로 설정하면 됩니다.
answer-filling은 evolving으로 만들어진 데이터들을 채우는 과정의 진행 여부를 결정하며 1이면 진행, 0이면 진행하지 않습니다.
마지막으로 생성된 세대만 저장하고 싶다면 save-last-gen을 1로 설정하면 됩니다.
temperature, max-tokens, top-p, timeout, max-retries는 child 생성시 모델의 설정 값으로 조절 가능합니다.
```bash
python main.py\
 --seed-path ./seed_instruction.json\
 --whole-path ./whole_generations.json\
 --failures-path ./failures.json\
 --total-gen 2\
 --batch-size 10\
 --save-last-gen 0\
 --save-location ./\
 --test-run 1\
 --answer-filling 1\
 --result-path ./koevol_result.json\
 --seed 42\
 --temperature 0.9\
 --max-tokens 2048\
 --top-p 0.9\
 --timeout 100\
 --max-retries 2
```

## Main Features
1. **Instruction Evolution**: 기존 instruction을 evolving 기법을 통해 더 복잡하고 상세한 형태로 진화시킵니다.
2. **Answer Filling**: 진화된 instruction에 대한 적절한 답변을 생성합니다.
3. **Error Handling**: evolution에 실패한 케이스들을 별도로 저장하여 추적이 가능합니다.

## Data Structure
```python
# Whole Generations
{
    "instruction": "...", # 진화된 instruction
    "output": "...", # 진화된 instruction에 대한 답변
    "generation": "...", # 세대
    "root": "...", # 초기 seed instruction의 출처
    "trace": "...", # 진화 과정(어떤 프롬프트를 통해 evolving 과정을 진행했는지)
    "origin": "..." # 초기 seed instruction
}
```
```python
# Failures
{
    "parent": "...", # 진화 과정에서의 부모 프롬프트
    "child": "...", # 진화 과정에서의 자식 프롬프트
    "generation": "...", # 세대
    "trace": "...", # 진화 과정(어떤 프롬프트를 통해 evolving 과정을 진행했는지)
    "origin": "..." # 초기 seed instruction
}
```

## Appendix

### Evolving Prompt
Depth evolution의 Complicating 프롬프트를 제외하고 모든 depth, breadth evolution 프롬프트는 논문에 나온 그대로 사용하였습니다.

### Commercial Usage of Data
이 레포에서 사용된 모든 데이터와 모델은 상업적 활용이 가능한 것들로만 구성했습니다.
데이터의 상업적 사용성을 유지하고 싶다면, 반드시 seed 데이터 및 생성 모델들을 상업적 사용이 가능한 것들로만 구성하세요.

### Evol-Instruct Process
논문에서 진행한 evolving 과정은 t세대에서 0~t-1세대의 모든 데이터를 활용하지만 이 레포에서는 t세대의 데이터를 만들 때 t-1세대의 데이터만을 활용합니다.

### Is it Work?
이 레포의 방식으로 생성된 데이터가 실제로 유용한지 확인하기 위해 Unsloth/Phi-4-bnb-4bit 모델에 다음 두 데이터셋을 활용한 fine-tuning을 진행하여 성능을 비교했습니다.
1. LIMA 데이터셋을 한국어로 번역한 데이터셋(https://huggingface.co/datasets/taeshahn/ko-lima)
2. 이 레포에서 생성한 데이터셋(https://huggingface.co/datasets/joonavel/ko-evol-instruct)

KMMLU 데이터셋을 활용하여 모델의 성능을 평가한 결과 이 레포에서 생성한 데이터셋을 활용한 모델이 더 높은 성능을 보였습니다.

**base model**: 0.468

**with kolima(epoch8)**: 0.494 https://huggingface.co/joonavel/Phi-4-kolima-adapter

**with koevol(epoch8)**: 0.499 https://huggingface.co/joonavel/Phi-4-koevol-adapter

## Cautions
- 테스트 실행을 통해 파라미터를 조정하는 것을 권장합니다.