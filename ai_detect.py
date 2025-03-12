from LLM.openaiUtils import *
from Config import *

conf = get_config()
openai_conf = conf['openai3']
openai_client = OpenAIUtils(base_url=openai_conf['base_url'], model_id=openai_conf['model_id'], generation_kwargs=openai_conf['generation_kwargs'], _api_key=openai_conf['api_key'])


if __name__ == "__main__":

    with open("data/input.txt", "r") as f:
        ai_prompts = f.readlines()
        for ai_prompt in ai_prompts:
            ai_prompt = ai_prompt.strip()
            # print(ai_prompt)
            if ai_prompt == "":
                continue
            print("AI检测")
            pro, msg = openai_client.cal_ai_prob(ai_prompt)
            print(f"Probability of prompt '{ai_prompt[:10]}...': {pro}")
            print(f"Response: {msg}")
            print("*"* 30 + "\n"*5)