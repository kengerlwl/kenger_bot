

# 访问
`http://127.0.0.1:5000/`
## TODO
### 3-1
目前只写了rag基本demo，
检索只实现了ES。
后端只实现了一个非流式的，没有上下文的，上下文建议先放前端，



# script
```
pytest -s test/test_ES.py::test_save_all_md_to_es
```


# TODO
ai detect: 将判断逻辑，改为判断后面词是否是大模型生成的最大概率的n个词。并且引入多次截断。取平均值。