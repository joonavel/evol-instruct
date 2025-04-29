#!/bin/bash

python main.py\
 --repo_names "HAERAE-HUB/KMMLU,beomi/KoAlpaca-v1.1a,HumanF-MarkrAI/WIKI_QA_Near_dedup"\
 --seed 42\
 --subset_ext_cnt 10\
 --ext_cnt 100\
 --save_path "../seed_instruction.json"