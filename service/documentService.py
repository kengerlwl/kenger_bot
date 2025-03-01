from entity import *
from mapper import *
from Kit import *
import os

def read_all_md(md_dir: str) -> List[Document]:
    documents = []
    for root, _, files in os.walk(md_dir):  # 遍历所有子目录
        print(f"Reading {root}")
        for md_file in files:
            if md_file.endswith(".md"):  # 只处理 Markdown 文件
                doc_id = str(uuid.uuid1())  # 生成唯一 ID
                file_path = os.path.join(root, md_file)  # 构造完整文件路径
                try:
                    doc = parse_markdown_metadata(file_path, doc_id)  # 解析 Markdown 元数据
                    doc.paragraph = parse_markdown(doc.content, doc.title)  # 解析 Markdown 内容
                    documents.append(doc)
                except Exception as e:
                    print(f"Error when reading {file_path}: {e}")
    return documents


# 实现， 读取所有md，然后存入es的功能。
def save_all_md_to_es(es_client: ESClient, index_name: str, md_dir: str):
    # 读取所有md文件
    documents = read_all_md(md_dir)
    print(f"Read {len(documents)} documents from {md_dir}")
    # 将每个md文件的内容存入ES
    for document in documents:
        print(f"Insert document {document.title} to ES")
        es_client.insert_document(index_name, document)
        # break
        # save_document(document, es_client, index_name)


# 传入一个Document，将其paragraph存入ES
def save_document(document: Document, es_client: ESClient, index_name: str):
    pass
    
    # paras = [document.paragraph]
    # while len(paras) > 0:
    #     para = paras.pop(0)
    #     es_client.insert_record(index_name, para.id, para.to_dict())
    #     paras.extend(para.sub_paragraph)
    #     # print(f"Insert paragraph {para.title} to ES")
        
