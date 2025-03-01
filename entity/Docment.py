
        
import yaml
import re
from typing import Dict, Any

# Document 类，表征一条文档记录
class Document:
    def __init__(self, doc_id: str, content: str, title: str, date: str, tags: list, categories: list, author: str):
        self.id = doc_id
        self.content = content
        self.title = title
        self.date = date
        self.tags = tags
        self.categories = categories
        self.author = author
        self.paragraph = None
    
    def to_dict(self) -> Dict[str, Any]:
        """将文档转为字典格式"""
        return {
            "id": self.id,
            "content": self.content,
            "title": self.title,
            "date": self.date,
            "tags": self.tags,
            "categories": self.categories,
            "author": self.author
        }