import aiohttp
import asyncio
from typing import List, Dict, Any
from openai import OpenAI
import functools
import numpy as np
import tiktoken
import json


class OpenAIUtils:
    def __init__(self, base_url: str, model_id: str, generation_kwargs: Dict[str, Any] = {}, _api_key: str = "EMPTY"):
        self._model_id = model_id
        self._generation_kwargs = generation_kwargs
        self._base_url = base_url
        self._api_key = _api_key

    def _sync_request(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        client = OpenAI(api_key=self._api_key, base_url=self._base_url)
        return client.chat.completions.create(
            model=self._model_id,
            **payload
        )

    # TODO: 计算分词，但是我的机器不行，太慢了，后序加入吧。
    @staticmethod
    def get_tokens(string, encoding_name) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(encoding_name)
        tokens = encoding.encode(string)
        # 复原为原始字符串
        tokens = [encoding.decode([token]) for token in tokens] 
        num_tokens = len(tokens)
        return num_tokens, tokens


    def get_text_ppl(self, text: str) -> float:
        """
        使用 OpenAI API 计算文本的困惑度 (Perplexity, PPL)。
        需要确保使用的 /completions 接口支持 logprobs 与 echo 参数。
        """
        
        prompt = f"请你帮我续写下面内容，```\n{text}\n```输出:"
        
        messages = [{"role": "user", "content": prompt}]
        payload = {
            "messages": messages,
            "logprobs": True,  # 启用 logprobs
            'top_logprobs': 10,
            'temperature': 1,
            'top_p': 1,
            "max_tokens": 1  # 确保能够处理整个文本
        }
        response = self._sync_request("/chat/completions", payload)
        # print(response)  # 调试打印 API 响应

        # print(response)  # 调试打印 API 响应

        # 确保 response 结构正确
        if not response.choices or not response.choices[0].logprobs:
            raise ValueError("API 响应缺少 logprobs 数据")

        # 提取 token 对数概率
        logprobs_data = response.choices[0].logprobs.content
        token_logprobs = [token_info.logprob for token_info in logprobs_data]
        # ChatCompletion(id='chatcmpl-tsnRDxkQqdfLHXh8ZrPHzO2Snsh5A', choices=[Choice(finish_reason='length', index=0, logprobs=ChoiceLogprobs(content=[ChatCompletionTokenLogprob(token='看', bytes=[231, 156, 139], logprob=-0.21946625, top_logprobs=[TopLogprob(token='看', bytes=[231, 156, 139], logprob=-0.21946625), TopLogprob(token='您', bytes=[230, 130, 168], logprob=-2.7194662), TopLogprob(token='很', bytes=[229, 190, 136], logprob=-4.094466), TopLogprob(token='抱', bytes=[230, 138, 177], logprob=-4.094466), TopLogprob(token='看来', bytes=[231, 156, 139, 230, 157, 165], logprob=-4.094466)])], refusal=None), message=ChatCompletionMessage(content='看', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))], created=1741801557, model='gpt-4o-mini', object='chat.completion', service_tier=None, system_fingerprint='fp_b705f0c291', usage=CompletionUsage(completion_tokens=1, prompt_tokens=23, total_tokens=24, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=None, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=None)))

        # 提取每个 token 对应的 top_logprobs
        top_tokens = [
            [(top_logprob.token, 100 * np.e ** top_logprob.logprob) for top_logprob in token_info.top_logprobs]  # 获取每个 token 的 top_logprobs 的 token 列表
            for token_info in logprobs_data
        ]
        tmp_tokens = {}
        for item in top_tokens[0]:
            i = item[0]
            j = item[1]
            print(item)
            tmp_tokens[i] = j
        # print(top_tokens)
        # 计算平均对数概率并据此计算困惑度
        avg_log_prob = np.mean(token_logprobs)
        ppl = np.exp(-avg_log_prob)
        
        
        rsp_msg = response.choices[0].message.content
        return ppl, response, rsp_msg, tmp_tokens


    # 通过第一个词的对数概率计算 AI 的回复概率，AI 的回复概率越高，AI 越有可能回答这个问题
    def cal_ai_prob(self, texts: str) -> float:
        
        texts = texts.split("\n")
        # 去除长度小于10的句子
        texts = [text for text in texts if len(text) > 10]
        sample_n = 5
        
        rsp = []
        for text in texts:
            text = text.strip()
            num_tokens, tokens = self.get_tokens(text, self._model_id)
            
            ai_prob = 0
            ai_probs = []
            # 从nums_tokens中的第10-90%的index的token中随机选择sample_n个token的index
            samples = np.random.choice(range(int(num_tokens * 0.1), int(num_tokens * 0.9)), sample_n, replace=False)
            print(f"num_tokens: {num_tokens}, samples: {samples}")
            # 得到n个前缀输入
            prefix_texts = ["".join(tokens[:sample]) for sample in samples]
            next_tokens = [tokens[sample] for sample in samples]
            # 将这n个前缀输入传入ppl计算函数中
            for index, prefix_text in enumerate(prefix_texts):
                now_prob = 0
                ppl, response, rsp_msg, top_tokens = self.get_text_ppl(prefix_text)
                target_token = next_tokens[index]
                
                if target_token in top_tokens:
                    now_prob = top_tokens[target_token]
                
                ai_prob+=now_prob    
                ai_probs.append(now_prob)
                # 判断 rsp_msg 是否是下一个token
                print(top_tokens)
                print(f"prefix_text: {prefix_text}, next_token: {next_tokens[index]} rsp_msg: {rsp_msg}")
            
            
            ai_prob = max(ai_probs) 
            rsp.append([ai_prob, str(top_tokens) + "\n" + str(ai_probs)])
            
        return rsp
        
        # ppl, response, rsp_msg, top_tokens = self.get_text_ppl(text)
        # logprobs_data = response.choices[0].logprobs.content
        # token_logprobs = [token_info.logprob for token_info in logprobs_data]

        # prob = 100 * np.e ** token_logprobs[0]
        
        # return prob, rsp_msg

    
    def get_chat_completion(self, messages: List[Dict[str, str]]) -> List[str]:
        payload = {
            "messages": messages,
            **self._generation_kwargs
        }
        response = self._sync_request("/chat/completions", payload)
        return response['choices'][0]['message']['content']
