#!/bin/bash

python main.py\
 --repo-names "HAERAE-HUB/KMMLU,beomi/KoAlpaca-v1.1a,HumanF-MarkrAI/WIKI_QA_Near_dedup"\
 --seed 42\
 --subset-ext-cnt 10\
 --ext-cnt 100\
 --save-path "../seed_instruction.json"