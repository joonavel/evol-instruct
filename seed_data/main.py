from huggingface_hub import login
from generate_seed import generate_seed
from dotenv import load_dotenv
import os, argparse


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_names",
                        type=str,
                        default="HAERAE-HUB/KMMLU,beomi/KoAlpaca-v1.1a,HumanF-MarkrAI/WIKI_QA_Near_dedup",
                        help="샘플링할 데이터셋 레포(HF), 쉼표로 구분, 기본은 KMMLU, KoAlpaca-v1.1a, WIKI_QA_Near_dedup")
    parser.add_argument("--seed",
                        type=int,
                        default=42,
                        help="Shuffle시 사용되는 seed")
    parser.add_argument("--subset_ext_cnt",
                        type=int,
                        default=10,
                        help="subset을 가지고 있는 데이터셋에서 subset 마다 샘플링할 데이터 수")
    parser.add_argument("--ext_cnt",
                        type=int,
                        default=100,
                        help="subset을 가지고 있지 않은 데이터셋에서 샘플링할 데이터 수")
    parser.add_argument("--save_path",
                        type=str,
                        default="../seed_instruction.json",
                        help="seed 데이터를 저장할 경로")
    return parser.parse_args()

if __name__ == "__main__":
    load_dotenv()
    login(token=os.getenv("MY_HF_TOKEN"))
    print("login 완료")
    config = get_config()
    config.repo_names = config.repo_names.split(",")
    generate_seed(config.repo_names, config.seed, config.subset_ext_cnt, config.ext_cnt, config.save_path)