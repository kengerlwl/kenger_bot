from LLM.openaiUtils import *
from Config import *

conf = get_config()
openai_conf = conf['openai3']
client = OpenAIUtils(base_url=openai_conf['base_url'], model_id=openai_conf['model_id'], generation_kwargs=openai_conf['generation_kwargs'], _api_key=openai_conf['api_key'])

# prompt = "What is the capital of China?"
ai_prompt = """
代码提交摘要（Commit Message: CM）是软件开发中用于描述代码变更的简要说明，对代码理解、协作和维护至关重要。尽管目前自动生成CM的方法已经有了进展，但仍存在许多挑战：首先现有的生成模型往往没有充分历史开发者的历史风格，导致生成CM不规范。其次是模型往往只能处理有限长度的输入，面对实际开发中的长代码提交往往束手无策。针对这些挑战，本文提出基于风格增强的CMG和基于大模型的多轮迭代评审推理的CMG，以提高生成CM的准确性和可读性。
"""

human_prompt = """
模型框架如图所示，首先通过向量嵌入模型输入Diff，检索出语义相似度高的Similar Message，然后通过BM25检索出关键词匹配高的Similar Message。最后，通过重排模型筛选出其中更有价值的Similar Message。接着，在风格增强生成模块中，将检索信息与代码diff分别输入Message Encoder和Diff  Encoder。然后经由协同注意力机制将这两个Message和Diff信息进行深度融合。息。最后，基于融合后的语义信息，模型在训练阶段引入基于Gram的风格损失函数，使得生成的Commit Message既准确又符合开发者个性化风格，全面提升生成质量和风格一致性。
"""
# import tiktoken

# # Try to list available encodings
# # print(tiktoken.registry.__dict__)

num, tokens = client.get_tokens(ai_prompt, "gpt-4o-mini")
print(num, tokens)

# # ai检测
# print("AI检测")
# pro, msg = client.cal_ai_prob(ai_prompt)
# print(f"Probability of prompt '{ai_prompt[:10]}...': {pro}")
# print(f"Response: {msg}")

# # human检测
# print("Human检测")
# pro, msg = client.cal_ai_prob(human_prompt)
# print(f"Probability of prompt '{human_prompt[:10]}...': {pro}")
# print(f"Response: {msg}")