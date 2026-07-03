# Codex 项目接续上下文

当前项目根目录：`D:\MedRag`

旧会话的原工作目录已经不存在。继续工作时不要读取或假设旧目录文件存在，应以当前项目结构为准。

当前代码状态：

1. 后端是 FastAPI 项目，入口为 `medrag/backend/main.py`。
2. 主要路由在 `medrag/backend/routers/pdf_router.py`。
3. 服务层已包含 PDF 上传解析、文本切分、embedding、Chroma 存储、检索、rerank、prompt 组装和大模型回答。
4. 前端是静态页面 `medrag/frontend/index.html`，调用 `/pdf/index`、`/pdf/search`、`/pdf/answer`。
5. 运行步骤和当前风险已整理到 `medrag/README.md`。

工作方式：

1. 默认中文回复，节约 Token。
2. 修改代码前先说明计划。
3. 每次只推进一个小任务。
4. 用户提交代码时优先审查，不直接重写。
5. 结尾给出下一步任务和相关面试追问。
