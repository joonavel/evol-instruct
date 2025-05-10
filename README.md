# koevol-instruct

[English](README.md) | [한국어](README.ko.md)

## Introduction
This repository implements an automated algorithm for augmenting Korean language data through instruction evolution, based on the evol-instruct (evolving) technique from the following paper:

WizardLM: Empowering Large Language Models to Follow Complex Instructions
(https://arxiv.org/abs/2304.12244)

## Installation
```bash
pip install -r requirements.txt
```

## Setting Environment Variables
Before running the project, you need to set the following environment variables in your .env file:
```
DEEPSEEK_API_KEY=your_deepseek_api_key
MY_HF_TOKEN=your_huggingface_api_key
```

## Project Structure
```
.
├── main.py              # Main execution file
├── evolving.py          # Instruction evolution logic
├── answer_filling.py    # Answer generation for evolved instructions
├── main.sh             # Execution script
├── requirements.txt     # Dependency package list
├── seed_instruction.json # Initial seed instruction data
├── prompts/            # Prompt templates directory
├── utils/              # Utility functions
└── seed_data/          # Directory for creating initial seed instructions
```

## Usage
The usage is as follows. Set test-run to 1 for test execution and 0 for actual execution.
answer-filling determines whether to proceed with filling in the evolved data (1 for proceed, 0 for skip).
If you want to save only the last generation, set save-last-gen to 1.
temperature, max-tokens, top-p, timeout, and max-retries are model configuration values that can be adjusted for creating child generations.
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
1. **Instruction Evolution**: Evolves existing instructions into more complex and detailed forms using the evolving technique.
2. **Answer Filling**: Generates appropriate answers for evolved instructions.
3. **Error Handling**: Tracks failed cases by storing them separately.

## Data Structure
```python
# Whole Generations
{
    "instruction": "...", # Evolved instruction
    "output": "...", # Answer to the evolved instruction
    "generation": "...", # Generation
    "root": "...", # Source of initial seed instruction
    "trace": "...", # Evolution process (which prompts were used in the evolving process)
    "origin": "..." # Initial seed instruction
}
```
```python
# Failures
{
    "parent": "...", # Parent prompt in evolution process
    "child": "...", # Child prompt in evolution process
    "generation": "...", # Generation
    "trace": "...", # Evolution process (which prompts were used in the evolving process)
    "origin": "..." # Initial seed instruction
}
```

## Appendix

### Evolving Prompt
All depth and breadth evolution prompts are used exactly as presented in the paper, except for the Complicating prompt in depth evolution.

### Commercial Usage of Data
All data and models used in this repository are composed of commercially available resources.
To maintain commercial usability of the data, ensure that seed data and generation models are composed only of commercially available resources.

### Evol-Instruct Process
While the paper's evolving process utilizes all data from generations 0 to t-1 when creating generation t, this repository only uses data from generation t-1 when creating generation t.

### Is it Work?
To verify the usefulness of data generated through this repository's method, we compared the performance of fine-tuning the Unsloth/Phi-4-bnb-4bit model using:
1. Korean-translated LIMA dataset (https://huggingface.co/datasets/taeshahn/ko-lima)
2. Dataset generated from this repository (https://huggingface.co/datasets/joonavel/ko-evol-instruct)

Using the KMMLU dataset for model evaluation, the model trained with our generated dataset showed higher performance:


**base model**: 0.468

**with kolima(epoch8)**: 0.494 https://huggingface.co/joonavel/Phi-4-kolima-adapter

**with koevol(epoch8)**: 0.499 https://huggingface.co/joonavel/Phi-4-koevol-adapter

## Cautions
- It is recommended to adjust parameters through test runs. 