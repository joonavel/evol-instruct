from huggingface_hub import login
from dotenv import load_dotenv
import os, argparse, getpass
from evolving import evolve
from answer_filling import answer_filling


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed-path',
                        type=str,
                        default='./seed_instruction.json',
                        help="seed 데이터가 저장된 경로"
                        )
    parser.add_argument('--whole-path', type=str, default='./whole_generations.json',
                        help="최종 결과가 저장된 경로"
                        )
    parser.add_argument('--failures-path', type=str, default='./failures.json',
                        help="실패한 결과가 저장된 경로"
                        )
    parser.add_argument('--total-gen', type=int, default=2,
                        help="진행할 세대 수"
                        )
    parser.add_argument('--batch-size', type=int, default=10,
                        help="배치 크기"
                        )
    parser.add_argument('--save-last-gen', type=int, default=0,
                        help="마지막 세대 저장 여부"
                        )
    parser.add_argument('--save-location', type=str, default='./',
                        help="결과가 저장될 경로"
                        )
    parser.add_argument('--test-run', type=int, default=1,
                        help="테스트 실행 여부"
                        )
    parser.add_argument('--answer-filling', type=int, default=1,
                        help="답변 채우기 여부"
                        )
    parser.add_argument('--result-path', type=str, default='./koevol_result.json',
                        help="답변까지 채운 결과가 저장될 경로"
                        )
    parser.add_argument('--seed', type=int, default=42,
                        help="랜덤 시드"
                        )
    parser.add_argument('--use-local', type=int, default=0,
                        help="로컬 모델 사용 여부"
                        )
    parser.add_argument('--use-deepseek', type=int, default=1,
                        help="DeepSeek 모델 사용 여부"
                        )
    parser.add_argument('--temperature', type=float, default=0.9,
                        help="데이터 생성시 온도"
                        )
    parser.add_argument('--max-tokens', type=int, default=2048,
                        help="데이터 생성시 최대 토큰 수"
                        )
    parser.add_argument('--top-p', type=float, default=0.9,
                        help="데이터 생성시 top_p"
                        )
    parser.add_argument('--timeout', type=int, default=100,
                        help="데이터 생성시 타임아웃"
                        )
    parser.add_argument('--max-retries', type=int, default=2,
                        help="데이터 생성시 최대 재시도 횟수"
                        )

    return parser.parse_args()

if __name__ == "__main__":
    config = get_config()
    
    load_dotenv()
    if not config.use_local and config.use_deepseek:
        if not os.getenv("DEEPSEEK_API_KEY"):
            os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")
    login(token=os.getenv("MY_HF_TOKEN"))

    print("Evolving...")
    evolve(seed_path=config.seed_path, whole_path=config.whole_path, failures_path=config.failures_path,
           total_gen=config.total_gen, batch_size=config.batch_size, seed=config.seed,
           save_location=config.save_location, save_last_gen=config.save_last_gen, test_run=config.test_run,
           temperature=config.temperature, max_tokens=config.max_tokens, top_p=config.top_p, timeout=config.timeout, max_retries=config.max_retries)
    
    if config.answer_filling:
        print("Answer filling...")
        answer_filling(whole_path=config.whole_path, save_path=config.result_path, batch_size=config.batch_size)
    

