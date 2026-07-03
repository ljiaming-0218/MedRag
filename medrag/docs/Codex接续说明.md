# Codex 接续说明

## 当前根目录

```text
D:\MedRag
```

旧会话的原工作目录已不存在。后续所有判断都应基于当前目录中的文件。

## 当前项目结构摘要

```text
D:\MedRag
├── AGENTS.md
├── .codex/
│   └── project-context.md
├── medrag/
│   ├── backend/
│   ├── frontend/
│   └── docs/
└── rag_tests/
```

## 已确认的后端能力

1. `GET /`：健康检查。
2. `POST /pdf/parse`：PDF 解析。
3. `POST /pdf/chunks`：文本切分。
4. `POST /pdf/index`：建立向量索引。
5. `POST /pdf/search`：检索文献片段。
6. `POST /pdf/prompt-preview`：预览 prompt。
7. `POST /pdf/answer`：生成回答。

## 运行步骤

```powershell
cd D:\MedRag\medrag\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

前端页面：

```text
D:\MedRag\medrag\frontend\index.html
```

## 需要注意

1. `backend/.env` 中不要提交真实 API key。
2. `backend/data/`、`rag_tests/chroma_data/` 是运行时数据。
3. 代码当前依赖本地 sentence-transformers 模型缓存。
4. 下一步优先补接口测试，确认 RAG 闭环可重复运行。
