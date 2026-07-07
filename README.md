---
title: DocRAG Agent
emoji: 🐢
colorFrom: yellow
colorTo: green
sdk: docker
pinned: false
short_description: 面向 PDF 文献阅读的 RAG 智能助手
app_port: 7860
---

# DocRAG Agent：面向 PDF 文献阅读的 RAG 智能助手

## 项目简介

DocRAG Agent 是一个面向 PDF 文献阅读的 RAG 智能助手。系统支持 PDF 文本解析、文本切分、向量化存储、语义检索、重排序、多轮问答和引用来源展示。

项目可用于学术论文、课程资料、技术文档、项目报告和政策文件等文本型 PDF。系统回答用于辅助阅读，重要结论应结合原始文档与引用来源核验。

## 在线演示

- Hugging Face Space：https://maoxiao-1205-medrag.hf.space/
- 免费实例可能存在冷启动，首次访问需要等待模型加载。

## RAG 流程

```text
上传 PDF
→ 按页解析文本
→ 文本切分
→ Embedding
→ Chroma 向量存储
→ Top-K 检索
→ CrossEncoder Rerank
→ 组装历史消息、文献片段和当前问题
→ 调用 LLM
→ 返回回答与引用来源
```

## 已实现功能

- PDF 上传、文本解析和页码保留
- `chunk_size`、`chunk_overlap` 文本切分
- 稳定的 `document_id` 和 chunk metadata
- BGE 中文 Embedding
- Chroma 向量持久化与文档过滤
- 向量召回和 CrossEncoder 重排序
- Prompt 模板管理
- OpenRouter/OpenAI-compatible API 调用
- MongoDB 会话与消息持久化
- 多轮问答和最近历史读取
- assistant 回答及 sources 保存
- FastAPI 同源托管 HTML 前端

## 技术栈

- 后端：Python 3.11、FastAPI、Uvicorn
- PDF：PyMuPDF
- Embedding：`BAAI/bge-small-zh-v1.5`
- Reranker：`BAAI/bge-reranker-base`
- 向量数据库：Chroma
- 会话数据库：MongoDB
- LLM：OpenRouter / OpenAI-compatible API
- 前端：HTML、CSS、JavaScript

## 目录结构

```text
MedRag/
├── medrag/
│   ├── backend/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── prompts/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── .env.example
│   ├── frontend/
│   │   ├── index.html
│   │   ├── app.js
│   │   └── styles.css
│   └── docs/
├── runtime/
├── rag_tests/
├── .gitignore
├── .dockerignore
└── AGENTS.md
```

## 环境配置

在 `medrag/backend` 下复制配置文件：

```cmd
copy .env.example .env
```

填写：

```env
OPENROUTER_API_KEY=your_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=your_model
CHROMA_DIR=<项目绝对路径>/runtime/chroma_db
UPLOAD_DIR=<项目绝对路径>/runtime/uploads
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_DB_NAME=medrag
```

`.env`、上传 PDF 和运行时数据库不得提交到 Git。

## 安装与启动

```cmd
conda activate medrag
cd /d D:\MedRag\medrag\backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

如果模型已缓存且 Hugging Face 网络不可用：

```cmd
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

访问：

- 前端：http://127.0.0.1:8000/
- Swagger：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

## 主要接口

| 接口 | 功能 |
| --- | --- |
| `POST /pdf/parse` | 解析 PDF 并返回分页文本 |
| `POST /pdf/chunks` | 返回切分后的文本块 |
| `POST /pdf/index` | 建立 PDF 向量索引 |
| `POST /pdf/search` | 检索相关文本块 |
| `POST /pdf/prompt-preview` | 查看 RAG Prompt |
| `POST /pdf/answer` | 单轮 RAG 问答 |
| `POST /conversations` | 创建会话 |
| `GET /conversations` | 获取会话列表 |
| `GET /conversations/{id}/messages` | 获取历史消息 |
| `POST /conversations/{id}/ask` | 在指定会话中继续提问 |

## 当前限制

- 主要支持文本型 PDF，扫描版 PDF 尚未接入 OCR。
- Chroma 使用本地文件持久化，免费云环境重启后可能丢失索引。
- 尚未实现 `user_id` 级用户隔离、历史文档管理和同文件识别。
- 多轮问答已保存近期历史，但尚未加入 Query Rewrite。
- 尚未建立完整的 RAG 评估集和自动化测试。
- 免费 Hugging Face Space 的启动速度和本地存储受平台资源限制。
- 不应上传包含隐私、商业机密或其他敏感信息的文档。

## 后续计划

- 增加轻量用户功能，实现 `user_id` 级文档和会话隔离。
- 通过 `document_hash` 识别同一用户重复上传的文档。
- 增加 Query Rewrite，将含指代的追问改写为独立检索问题。
- 根据 `user_type` 调整回答粒度和侧重点。
- 实现轻量 Agent Router 和文献阅读报告工具。
- 建立小型 RAG 评估集，评估检索相关性、答案忠实度、引用准确性和幻觉情况。
- 增加接口与业务层自动化测试。
