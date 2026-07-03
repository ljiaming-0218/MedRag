# MedRAG 医学文献问答系统

## 项目定位

MedRAG 是一个面向医学 PDF 文献辅助阅读的 RAG 项目。当前代码已经覆盖：

1. PDF 上传与解析
2. 文本切分
3. embedding 生成
4. Chroma 向量库持久化
5. 向量检索与 rerank
6. RAG prompt 组装
7. OpenRouter/OpenAI-compatible API 问答
8. 简单 HTML 前端演示

本项目只用于医学文献辅助阅读，不提供临床诊断或治疗建议。

## 当前项目根目录

```text
D:\MedRag
```

旧会话中的原工作目录不再作为依据。继续开发前应先读取当前目录结构。

## 目录结构

```text
D:\MedRag
├── AGENTS.md
├── medrag/
│   ├── backend/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   ├── prompts/
│   │   │   └── medical_qa_prompt.txt
│   │   ├── routers/
│   │   │   └── pdf_router.py
│   │   ├── services/
│   │   │   ├── pdf_upload.py
│   │   │   ├── pdf_service.py
│   │   │   ├── text_splitter.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store_service.py
│   │   │   ├── search_service.py
│   │   │   ├── rerank_service.py
│   │   │   ├── prompt_service.py
│   │   │   └── llm_service.py
│   │   └── data/
│   │       ├── uploads/
│   │       └── chroma_db/
│   ├── frontend/
│   │   └── index.html
│   └── docs/
└── rag_tests/
```

## 后端接口

| 接口 | 作用 |
| --- | --- |
| `GET /` | 健康检查 |
| `POST /pdf/parse` | 上传 PDF 并返回页码与文本 |
| `POST /pdf/chunks` | 上传 PDF 并返回切分后的 chunk |
| `POST /pdf/index` | 上传 PDF、切分、embedding、写入 Chroma |
| `POST /pdf/search` | 按 `document_id` 和问题检索相关 chunk |
| `POST /pdf/prompt-preview` | 查看 RAG prompt 组装结果 |
| `POST /pdf/answer` | 检索文献片段并调用大模型生成回答 |

## 环境配置

复制环境变量样例：

```powershell
Copy-Item .env.example .env
```

然后在 `backend/.env` 中填写：

```text
OPENROUTER_API_KEY=你的密钥
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=你的模型名
CHROMA_DIR=D:\medrag_runtime\chroma_db
```

注意：`.env` 不应提交到版本库。

## 启动

```cmd
conda activate medrag
cd /d D:\MedRag\medrag\backend
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

访问：http://127.0.0.1:8000/

## 当前重点

下一阶段优先做工程化收口，而不是继续堆功能：

1. 确认 embedding/rerank 模型是否已在本地缓存，否则 `local_files_only=True` 会启动失败。
2. 给 `/pdf/index`、`/pdf/search`、`/pdf/answer` 做最小接口测试。
3. 梳理 `document_id`、chunk id、Chroma 覆盖写入的稳定性。
4. 避免把真实 API key、上传 PDF、Chroma 数据提交到版本库。
