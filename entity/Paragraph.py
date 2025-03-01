from typing import Dict, Any

# Document 类，表征一条文档记录
class Paragraph:
    def __init__(self, doc_id: str, content: str, title: str, title_list = [], sub_paragraph = []):
        self.id = doc_id
        # 这段的内容
        self.content = content
        
        # 这段的子标题
        self.title = title
        
        # 从根节点下来的title_list
        self.title_list = title_list
        
        # 该段的子标题
        self.sub_paragraph = sub_paragraph
        
    def __mixed_content(self):
        return "#" * len(self.title_list)  + self.title + "\n内容：" + self.content
    
    def __title_chain(self):
        return " -> ".join(self.title_list + [self.title])

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.__mixed_content(),
            "title": self.__title_chain(),
        }