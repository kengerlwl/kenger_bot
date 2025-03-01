import sys

# 将命令行的目录加入模块搜索范围
sys.path.append('.')

import yaml
import re
from entity import Document, Paragraph

def parse_markdown_metadata(file_path, doc_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 仅匹配文章最开始的 YAML Front Matter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid Markdown format: Missing YAML Front Matter")
    
    yaml_content, markdown_content = match.groups()
    metadata = yaml.safe_load(yaml_content)  # 解析 YAML 元数据
    
    # 创建 Document 实例
    document = Document(
        doc_id=doc_id,
        content=markdown_content.strip(),
        title=metadata.get('title', ''),
        date=metadata.get('date', ''),
        tags=metadata.get('tags', []),
        categories=metadata.get('categories', []),
        author=metadata.get('author', 'Unknown')
    )
    
    return document


import re
import uuid
from typing import List


def parse_markdown(md_text: str, doc_title="doc title") -> Paragraph:
    root = Paragraph(doc_id="root", content="", title=doc_title, title_list=[], sub_paragraph=[])
    stack = [(0, root)]
    lines = md_text.splitlines()
    content_lines = []
    in_code_block = False
    header_pattern = re.compile(r'^ {0,3}(#{1,6})\s+(.*)')  # 允许前导空格且#后必须有空格
    
    for line in lines:
        stripped_line = line.rstrip()
        
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            content_lines.append(line)
            continue
        
        if not in_code_block:
            header_match = header_pattern.match(stripped_line)
            if header_match:
                # 获取父节点
                parent = stack[-1][1] if stack else root
                
                # 保存累积的内容
                if content_lines:
                    combined = "\n".join(content_lines).strip()
                    if parent.content:
                        parent.content += "\n" + combined
                    else:
                        parent.content = combined
                    content_lines = []
                
                # 处理新标题
                hashes, title_text = header_match.groups()
                title_text = title_text.strip()
                level = len(hashes)
                
                # 更新栈结构
                while stack and stack[-1][0] >= level:
                    stack.pop()
                
                # 创建新段落
                parent_titles = [p.title for lvl, p in stack if lvl < level]
                new_para = Paragraph(
                    doc_id=str(uuid.uuid4()),
                    content="",
                    title=title_text,
                    title_list=parent_titles,
                    sub_paragraph=[]
                )
                
                # 添加到父节点
                current_parent = stack[-1][1] if stack else root
                current_parent.sub_paragraph.append(new_para)
                stack.append((level, new_para))
                continue
        
        # 普通内容行
        content_lines.append(line)
    
    # 处理剩余内容
    if content_lines:
        parent = stack[-1][1] if stack else root
        combined = "\n".join(content_lines).strip()
        if parent.content:
            parent.content += "\n" + combined
        else:
            parent.content = combined
    
    return root

# 示例使用
if __name__ == "__main__":
    md_example = """
开头的一些介绍文字，未使用标题。
这部分内容将挂在根节点上。

# 第一章 标题1
这是一段第一章的内容。
```
代码块示例：
# sdf
print("Hello World")
```

## 小节 标题1.1
这是小节下的内容。

sdfas

### 1.1.1
adfs

## 1.2

### 1.2.1

# 第二章 标题2
这是第二章的内容。
    """.strip()

    file_path = "/home/kenger/kenger_aibot/data/大模型agent框架调研.md"  # 替换为你的Markdown文件路径
    doc = parse_markdown_metadata(file_path, "doc_001")
    # print(doc.to_dict())
    
    root_paragraph = parse_markdown(doc.content, doc.title)
    
    def print_paragraph(p: Paragraph, indent=0):
        print(" " * indent + f"标题: {p.title}")
        print(p.title_list)
        if p.content:
            print(" " * (indent + 2) + f"内容: {p.content}")
        for sub in p.sub_paragraph:
            print_paragraph(sub, indent + 4)
    
    print_paragraph(root_paragraph)


# 示例调用
if __name__ == "parase_md":
    file_path = "/home/kenger/kenger_aibot/data/自部署并发调查.md"  # 替换为你的Markdown文件路径
    doc = parse_markdown_metadata(file_path, "doc_001")
    print(doc.to_dict())
