import sys
sys.path.append('.')
from Kit.connector import es_client, ESClient
import os


from typing import List, Dict
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

from langchain.globals import set_verbose

set_verbose(True)
from langchain.globals import set_debug

set_debug(True)


# 自定义Retriever（继承BaseRetriever）
from langchain.schema import Document
from typing import List

class ESRetriever(BaseRetriever):
    def __init__(self, es_client: ESClient, index_name: str = "kenger_blog"):
        super().__init__()
        self._es_client = es_client  # 用 `_` 作为私有属性
        self._index_name = index_name
        # self._top_k = 3

    @property
    def es_client(self):
        """提供一个受控访问的 `es_client`"""
        return self._es_client
    
    @property
    def index_name(self):
        return self._index_name

    def _get_relevant_documents(self, query: str, *, top_k: int = 10) -> List[Document]:
        
        
        # print(f"查询内容: {query}")
        
        # 使用 self.es_client 进行查询
        results = self.es_client.search_by_content(self.index_name, query, top_k)
        
        # print(f"查询结果: {results}")
        # 针对同一个id_前缀的.进行排序。先把若干para分成doc，然后对doc进行排序
        docs = {}
        for para in results:
            id = para["id"]
            doc_id = id.split("_")[0]
            docs[doc_id] = docs.get(doc_id, []) + [para]
        
        # 对doc进行排序
        for doc_id, paras in docs.items():
            paras.sort(key=lambda x: x["id"])
        
        final_res = ""          
        for doc_id, paras in docs.items():
            doc_title = paras[0]["title"].split("->")[0]
            final_res += f"文档：{doc_title}\n"
            for para in paras:
                final_res += para["content"] + "\n"
            
        return final_res
        

# 示例：使用ChatGPT
from langchain_openai import ChatOpenAI
from Config import get_config
conf = get_config()
openai_conf = conf["openai3"]

# 配置本地LLM服务（示例适用于Ollama）
openai_llm = ChatOpenAI(
    model=openai_conf['model_id'],  # 根据实际模型名称修改
    base_url=openai_conf['base_url'],  # 本地服务地址
    api_key= openai_conf['api_key'] ,  # 虚拟key（某些本地服务可任意填写）
    temperature=openai_conf['generation_kwargs']['temperature'],  # 温度参数
    
)



# 初始化组件
retriever = ESRetriever(es_client=es_client, index_name="kenger_blog")

# 构建提示模板
template = """你是kenger的博客搜索助手，请你根据检索到的内容回答问题：
检索到的文档
{context}

问题：{question}
要求：
1. 用户是看不到检索到的文档的，所以你需要根据检索到的内容回答问题。
2. 请你尽可能根据检索到的内容回答问题。
3. 如果无法从上下文得到答案，请直接说不知道。"""
prompt = ChatPromptTemplate.from_template(template)

# 定义处理链
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | openai_llm  # 替换为实际LLM（如ChatOpenAI、Ollama等）
    | StrOutputParser()
)

# 使用示例
# question = input("请输入问题：")

if __name__ == "__main__":
    question = "cors 跨域改如何解决， 请你给出具体代码"
    question = "1"
    answer = rag_chain.invoke(question)
    print(f"问题：{question}\n答案：{answer}")