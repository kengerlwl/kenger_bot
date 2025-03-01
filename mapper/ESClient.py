import sys
# 将命令行的目录加入模块搜索范围
sys.path.append('.')
from elasticsearch import Elasticsearch, exceptions
from typing import Optional, List, Dict, Any
from entity import Document, Paragraph

# Elasticsearch 客户端
class ESClient:
    def __init__(self, host: str = 'localhost', port: int = 9200, username: str = "elastic", password: str = ""):
        self.es = Elasticsearch(
            [{'host': host, 'port': port, "scheme":"http"}],
            http_auth=(username, password)  # 传入用户名和密码
        )    
    def create_index(self, index_name: str, mapping: Dict[str, Any]) -> bool:
        """创建索引"""
        if not self.es.indices.exists(index=index_name):
            try:
                self.es.indices.create(index=index_name, body=mapping)
                return True
            except exceptions.RequestError as e:
                print(f"索引创建失败: {e}")
                return False
        return False
    
    
    # TODO: md的标题链式应该加入以提高检索准确率
    def insert_record(self, index_name: str, doc_id: str, record: Dict[str, Any]) -> bool:
        """新增文档"""
        try:
            self.es.index(index=index_name, id=doc_id, body=record)
            return True
        except Exception as e:
            print(f"文档插入失败: {e}")
            return False
    
    # 批量插入记录，以文档为单位。
    def insert_document(self, index_name: str, document: Document) -> bool:
        """将文档及其段落结构插入ES"""
        # 平铺所有段落（包含嵌套子段落）
        def flatten_paragraphs(paragraph: Paragraph) -> list:
            """递归展开段落结构"""
            
            paragraphs = []
            queue = [paragraph]
            while queue:
                para = queue.pop(0)
                paragraphs.append(para)
                queue.extend(para.sub_paragraph)
            return paragraphs
        
        try:
            # 生成平铺段落列表
            all_paragraphs = flatten_paragraphs(document.paragraph) if document.paragraph else []
            bulk_data = []

            for idx, para in enumerate(all_paragraphs):
                # 生成唯一ID和基础数据
                para_id = f"{document.id}_{idx}"
                record = para.to_dict()
                
                # 构建批量操作格式
                bulk_data.append({"index": {"_id": para_id}})
                bulk_data.append(record)

            # 执行批量插入
            if bulk_data:
                response = self.es.bulk(
                    index=index_name,
                    body=bulk_data,
                    refresh=True  # 可选：立即刷新可见
                )
                
                # 检查错误（关键错误处理）
                if response.get("errors"):
                    for item in response["items"]:
                        if "error" in item["index"]:
                            print(f"插入失败: {item['index']['error']}")
                    return False
                return True
            return False  # 无段落可插入
        except Exception as e:
            print(f"文档插入失败: {e}")
            return False
        
        
            
    def get_record(self, index_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """查询文档"""
        try:
            result = self.es.get(index=index_name, id=doc_id)
            return result['_source']
        except exceptions.NotFoundError:
            print(f"文档 {doc_id} 未找到")
            return None
        except exceptions.ElasticsearchException as e:
            print(f"查询文档失败: {e}")
            return None
        
    
    def update_record(self, index_name: str, doc_id: str, record: Dict[str, Any]) -> bool:
        """更新文档"""
        try:
            self.es.update(index=index_name, id=doc_id, body={"doc": record})
            return True
        except exceptions.ElasticsearchException as e:
            print(f"文档更新失败: {e}")
            return False
    

    
    def delete_record(self, index_name: str, doc_id: str) -> bool:
        """删除文档"""
        try:
            self.es.delete(index=index_name, id=doc_id)
            return True
        except exceptions.NotFoundError:
            print(f"文档 {doc_id} 未找到，无法删除")
            return False
        except exceptions.ElasticsearchException as e:
            print(f"文档删除失败: {e}")
            return False
    
    def search(self, index_name: str, query: Dict[str, Any], size: int = 10) -> List[Dict[str, Any]]:
        """查询文档"""
        try:
            response = self.es.search(index=index_name, body=query, size=size)
            return [hit['_source'] for hit in response['hits']['hits']]
        except Exception as e:
            print(f"查询失败: {e}")
            return []


    def search_by_content(self, index_name: str, content: str, size: int = 10) -> List[Dict[str, Any]]:
        """根据内容查询文档"""
        query = {
            "query": {
                "match": {
                    "content": content
                }
            }
        }
        return self.search(index_name, query, size)
    
    
    def search_by_title(self, index_name: str, title: str, size: int = 10) -> List[Dict[str, Any]]:
        """根据标题查询文档"""
        query = {
            "query": {
                "match": {
                    "title": title
                }
            }
        }
        return self.search(index_name, query, size)




# 测试代码
if __name__ == "__main__":
    es_client = ESClient(host="127.0.0.1", password="WKcqDgd8k5WgF2Xp2koj")

    # 定义索引映射
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "content": {"type": "text"},
                "title": {"type": "text"}
            }
        }
    }

    # 创建索引
    # es_client.create_index('kenger_blog', mapping)

    # 创建一个文档实例
    # doc = Document(doc_id="3", content="这是一个关于人工智能的博客文章，详细介绍了深度学习。", title="人工只能与深度学习概述")
    para = Paragraph(doc_id="3", content="这是一个关于人工智能的博客文章，详细介绍了深度学习", title="这是一个关于人工智能的博客文章，详细介绍了深度学习")

    # 新增文档
    es_client.insert_record('kenger_blog', para.id, para.to_dict())

    # 查询文档
    result = es_client.get_record('kenger_blog', para.id)
    print("查询结果:", result)

    # 更新文档
    update_data = {"content": "这是更新后的机器学习文章内容，新增深度学习相关内容。"}
    es_client.update_record('kenger_blog', para.id, update_data)

    # 删除文档
    # es_client.delete_document('kenger_blog', doc.id)

    # 搜索文档
    query = {
        "query": {
            "multi_match": {
                "query": "深度学习",
                "fields": ["content", "title"]
            }
        }
    }
    search_results = es_client.search('kenger_blog', query)
    print("搜索结果:", search_results)
