# RAG 模块

## 功能1：知识库向量化

**输入参数**：json化的知识库

**输出参数**：向量化的知识库

**功能详述**：将json数据库向量化，将文本内容转换成数据想想存储再vector database中，向量数据库可选择Milvus。

**举例**：

| 文本知识库   |  |
|--------|------|
| {<br> "question": "...",<br>"answer": ["..."],<br>"positive_contexts": [{ "content": "...", "source": "..." }],<br>"category": "...",<br>"type": "Basic"<br>} | [<br> 0.01234, -0.07845, 0.09231, ..., 0.00323<br>]  |


