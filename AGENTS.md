# DocRAG Agent 项目 Codex 协作规则

你现在是我的 DocRAG Agent 项目开发助教、代码审查员和大厂实习面试训练官。请严格围绕“把已有 RAG Demo 打磨成可投大模型应用开发实习的工程项目”来协助我。

不要一次性重构整个项目，不要随意加入与当前阶段无关的复杂功能。每次只处理一个明确阶段，优先保证已有 RAG 主链路稳定。

---

## 一、项目背景

项目名称：

DocRAG Agent：面向 PDF 文献阅读的 RAG 智能助手。

当前项目已有基础 RAG 流程，包括：

* PDF 上传
* 文本解析
* 文本切分
* 向量化
* 向量检索
* 大模型回答
* 引用来源 sources 展示
* 前端展示
* 基础在线部署

项目基础功能已经测试完毕。

后续目标是将项目从“能跑的 RAG Demo”升级为“能被大厂实习面试深挖的大模型应用工程项目”。

目标岗位：

* 大模型应用开发实习
* AI 应用开发实习
* RAG 开发实习
* Agent 开发实习
* AI 后端开发实习

重点面向成都互联网大厂或准大厂。

---

## 二、项目定位

项目统一定位为：

DocRAG Agent：面向 PDF 文献阅读的 RAG 智能助手。

不要再将项目固定为“医学文献问答系统”。本项目是通用 PDF 文献问答助手，可用于：

* 学术论文
* 课程资料
* 技术文档
* 项目报告
* 政策文件
* 招标文件
* 医学文献

医学文献只能作为测试样例之一，不能把系统定位写死在医学场景。

如果页面、README、接口描述、提示词、变量命名中出现 MedRAG、医学文献、医学文献问答系统等旧定位，请提醒我统一改成：

* DocRAG
* 文献问答助手
* PDF 文献阅读助手
* 文档知识库问答助手

线上展示页面中不要出现“在 backend 目录运行 uvicorn main:app --reload”这类本地开发提示。线上页面应展示为正式演示版。

---

## 三、当前最高优先级

后续开发按下面顺序推进，不要平均用力：

1. 统一项目定位：从 MedRAG 医学文献改成 DocRAG 通用文献问答助手。
2. 删除线上页面中的本地开发提示。
3. 增加轻量用户功能：先创建/选择用户，再确定用户类型。
4. 实现用户隔离：user_id 关联 document、conversation、message。
5. 实现 document_hash：识别同一用户是否上传过同一份 PDF。
6. 实现历史会话列表：同一用户上传同一文件时能展示历史对话。
7. 实现单次对话记忆：同一 conversation 内读取最近 3-5 轮历史。
8. 实现 Query Rewrite：根据历史将追问改写成适合检索的独立问题。
9. 确保 assistant 回答对应的 sources 能随 message 保存。
10. 实现用户分类 Prompt：不同用户类型对应不同回答策略。
11. 新增 Agent Router，先实现“阅读报告生成”工具。
12. 构建 RAG 小型评估集。
13. 补充工程化细节：异常处理、日志、API Key 安全、README、接口文档。
14. 最后再考虑 rerank、hybrid search、流式输出等加分项。

---

## 四、暂时不要优先做的内容

当前 DocRAG 项目暂时不要加入以下内容：

* 多 Agent 协作
* MCP
* Skills 文件系统
* 复杂权限系统
* 多租户
* Docker Compose 全家桶
* 复杂后台管理
* 联网检索论文
* 模型微调
* Text2SQL
* 岗位 JD 分析或模拟面试

这些内容后续会放在另一个项目 OfferPilot MCP 中。

DocRAG 当前只专注于：

* RAG
* PDF 文献问答
* 用户隔离
* 会话记忆
* Query Rewrite
* 用户分类 Prompt
* 阅读 Agent
* RAG 评估
* 工程化

---

## 五、用户功能设计：先创建用户，再确定用户类型

当前阶段应从“单用户演示版”升级为“支持用户隔离和用户画像的文献问答系统”。

建议先实现轻量用户功能，不要一开始做完整登录注册系统。

第一版用户逻辑：

1. 用户进入页面时，先创建用户或选择已有用户。
2. 用户创建时填写 username。
3. 用户创建时选择默认 user_type。
4. 前端用 localStorage 保存当前 user_id。
5. 后端所有 document、conversation、message 都必须关联 user_id。
6. 切换用户后，只加载该用户自己的文档和历史对话。

不要先做：

* 密码登录
* JWT
* OAuth
* 手机验证码
* 复杂权限系统

后续项目正式化时，再扩展登录注册和鉴权。

---

## 六、用户类型设计

用户类型应作为用户画像的一部分，而不是每次提问时临时随便传。

建议用户类型：

* undergraduate：本科生
* graduate_student：研究生
* researcher：科研人员
* developer：工程开发者
* teacher：教师
* general：普通用户

用户类型作用：

undergraduate：
少术语，多解释基础概念，语言更通俗。

graduate_student：
强调研究问题、方法路线、实验设计、创新点和局限性。

researcher：
强调相关工作、方法贡献、实验设置、可复现性和局限。

developer：
强调实现流程、技术路线、数据处理、系统落地和工程实现。

teacher：
强调知识结构、教学讲解、可提问点和课堂表达。

general：
简洁概括，减少专业细节。

---

## 七、用户类型的继承与覆盖规则

用户类型建议分三层：

### 第一层：用户默认类型

users 表中保存 default_user_type。

例如：

* 用户 A 默认是 graduate_student
* 用户 B 默认是 developer

### 第二层：对话快照类型

conversation 创建时，默认继承当前用户的 default_user_type，并保存为 conversation.user_type。

这样做的好处是：

即使用户之后修改了自己的默认类型，旧对话仍然保持创建时的回答风格，避免历史对话前后不一致。

### 第三层：前端临时回答模式

前端可以做一个类似 ChatGPT / DeepSeek 的“回答模式”选择器。

例如：

* 当前用户：李佳茗
* 默认身份：研究生
* 当前对话模式：研究生
* 可切换为：本科生 / 研究生 / 科研人员 / 工程开发者 / 教师 / 普通用户

当用户切换模式时，前端应提供两种选择：

1. 仅应用到当前对话。
2. 更新为当前用户的默认类型。

优先级建议：

本次请求显式传入的 user_type

> conversation.user_type
> user.default_user_type
> general

也就是：

1. 本次请求临时指定了 user_type，就用本次的。
2. 如果没有临时指定，就用当前 conversation 的 user_type。
3. 如果 conversation 没有，就用 user 的 default_user_type。
4. 如果用户也没有设置，就用 general。

---

## 八、用户数据结构建议

users:

* user_id
* username
* default_user_type
* created_at
* updated_at

documents:

* document_id
* user_id
* document_hash
* filename
* title
* created_at
* updated_at

conversations:

* conversation_id
* user_id
* document_id
* document_hash
* title
* user_type
* created_at
* updated_at

messages:

* message_id
* conversation_id
* role
* content
* rewritten_query
* sources
* created_at

字段含义：

* user_id 用于隔离不同用户。
* document_id 用于区分不同文档。
* document_hash 用于识别同一份 PDF。
* conversation_id 用于区分同一用户在同一文档下的不同对话。
* user_type 用于控制回答风格。
* rewritten_query 用于保存 Query Rewrite 结果。
* sources 必须随 assistant message 保存。

---

## 九、同一文件历史对话识别

上传 PDF 时，后端应计算文件 hash，例如 sha256。

如果用户上传同一份文件，系统应识别：

1. 当前 user_id 是否已经上传过相同 document_hash。
2. 如果上传过，前端展示该文件对应的历史 conversation 列表。
3. 用户可以选择继续某个历史对话。
4. 用户也可以选择基于该文件新建对话。
5. 不要重复索引相同文件，除非用户明确选择重新索引。

建议流程：

用户上传 PDF
→ 后端计算 document_hash
→ 根据 user_id + document_hash 查询是否已有 document
→ 如果已有，返回 existing_document=true 和历史 conversation 列表
→ 前端展示“检测到该文件已有历史对话”
→ 用户选择继续历史对话或新建对话

返回结构参考：

```json
{
  "document_id": "xxx",
  "document_hash": "xxx",
  "existing_document": true,
  "conversations": [
    {
      "conversation_id": "xxx",
      "title": "关于本文方法的讨论",
      "updated_at": "2026-xx-xx"
    }
  ]
}
```

---

## 十、会话记忆设计要求

DocRAG 必须真实落地会话记忆，而不是只在页面上写概念。

需要实现或检查以下能力：

1. 每次上传文献生成 document_id。
2. 每次新建问答生成 conversation_id。
3. 每轮用户问题保存成 user message。
4. 每轮模型回答保存成 assistant message。
5. assistant message 必须保存 sources。
6. 刷新页面后能恢复历史消息。
7. 用户追问时能读取最近几轮历史。
8. 不要把全部历史无限塞进 prompt。
9. 第一版只取最近 3-5 轮作为短期上下文。
10. 回答事实性问题时，仍然以当前问题检索到的文献片段作为主要依据。
11. 如果历史和文献检索结果冲突，以文献检索结果为准。

面试表达要点：

我没有把所有历史都塞进 Prompt，而是只取最近几轮对话作为短期上下文；历史用于理解当前问题，文献检索结果才是事实依据。

---

## 十一、Query Rewrite 设计

为支持多轮追问，需要新增 Query Rewrite 模块。

作用：

将用户的当前追问，结合最近几轮历史，改写成一个更完整、适合检索的独立问题。

示例：

历史：
用户：这篇论文主要提出了什么方法？
助手：本文提出了一种基于 Transformer 的文献问答方法。

当前问题：
它的创新点是什么？

改写后：
这篇论文提出的基于 Transformer 的文献问答方法有哪些创新点？

新增函数建议：

rewrite_query(conversation_id: str, query: str) -> str

输入：

* conversation_id
* 当前 query
* 最近几轮历史消息

输出：

* rewritten_query

要求：

1. Query Rewrite 只用于检索，不直接替代用户原始问题展示。
2. 前端仍展示用户原始问题。
3. 后端保存 rewritten_query，便于调试和评估。
4. 如果用户问题已经足够完整，可以保持原问题不变。
5. Query Rewrite 不能引入文献中没有的信息。
6. Query Rewrite Prompt 要求模型只补全指代和上下文，不要扩展事实。
7. rewritten_query 用于向量检索。
8. 原始 query 用于前端展示和消息保存。

Query Rewrite Prompt 参考：

```text
你是一个 RAG 检索查询改写助手。
你的任务是根据最近对话历史，将用户当前问题改写成一个完整、清晰、适合文献检索的独立问题。

要求：
1. 只补全必要的指代和上下文。
2. 不要添加对话中没有出现的新事实。
3. 不要回答问题。
4. 如果当前问题已经完整，直接返回原问题。
5. 输出只包含改写后的问题。

最近对话：
{history}

用户当前问题：
{query}

改写后的问题：
```

---

## 十二、加入用户、记忆和 Query Rewrite 后的问答流程

新的 /ask 流程应调整为：

1. 获取 user_id、conversation_id、document_id、query、user_type。
2. 校验 conversation 是否属于当前 user_id。
3. 保存用户原始问题。
4. 读取当前 conversation 最近 3-5 轮历史。
5. 使用 Query Rewrite 将当前问题改写为 rewritten_query。
6. 使用 rewritten_query 进行向量检索。
7. 获取相关 chunks 和 sources。
8. 根据 user_type、历史上下文、检索 chunks 组装 prompt。
9. 调用大模型生成回答。
10. 保存 assistant message，包括 answer、sources、rewritten_query。
11. 返回 answer、sources、conversation_id、rewritten_query。

注意：

* 原始 query 用于前端展示。
* rewritten_query 用于检索和调试。
* sources 用于答案追溯。
* history 用于理解上下文，但不能替代文献依据。
* 如果检索不到相关内容，应明确提示“根据当前文献内容无法确定”，不要编造。

---

## 十三、用户分类 Prompt 要求

Prompt 中需要明确加入当前用户类型和回答要求。

示例：

```text
当前用户类型：研究生。

回答要求：
请重点说明研究问题、方法路线、实验设计、创新点和局限性。

请只根据检索到的文献片段回答。
如果当前文献内容不足以回答，请说明“根据当前文献内容无法确定”，不要编造。
```

后端请求结构可参考：

```json
{
  "user_id": "xxx",
  "document_id": "xxx",
  "conversation_id": "xxx",
  "user_type": "graduate_student",
  "query": "总结这篇文献的方法"
}
```

---

## 十四、Agent Router 设计要求

当前只做单 Agent + 多工具，不要做复杂多 Agent。

Agent Router 第一版可以用规则实现，不必一开始就让 LLM 自主规划。

建议工具：

1. qa_tool：普通文献问答。
2. summary_tool：生成文献摘要。
3. term_tool：提取关键词和术语。
4. report_tool：生成阅读报告。
5. source_check_tool：引用检查或证据检查。

Router 第一版规则：

* 用户问题包含“总结、摘要、概括” → summary_tool
* 用户问题包含“术语、关键词、概念” → term_tool
* 用户问题包含“阅读报告、分析这篇文献” → report_tool
* 用户问题包含“依据、出处、引用、来源” → source_check_tool
* 其他情况 → qa_tool

第二版可以升级为 LLM 输出 JSON，例如：

```json
{
  "task": "report",
  "reason": "用户要求生成阅读报告"
}
```

Agent 的核心表达是：

基础 RAG 是固定流程，不管用户问什么都走“检索 + 回答”；Agent 版增加任务识别和工具选择能力，可以根据用户意图选择问答、摘要、术语提取、阅读报告等工具。所有工具底层仍然依赖文档检索和 sources，避免模型脱离原文生成。

---

## 十五、阅读报告工具要求

优先实现 report_tool，即“阅读报告生成工具”。

输入：

* document_id
* conversation_id
* user_type
* query
* top_k

输出结构建议：

1. 文献主题
2. 研究背景
3. 研究问题
4. 方法路线
5. 实验设计或案例
6. 主要结论
7. 创新点
8. 局限性
9. 适合继续追问的问题
10. 引用来源 sources

要求：

1. 必须基于检索片段生成。
2. 必须返回 sources。
3. 如果文献中没有相关内容，要标注“当前文献未提及”。
4. 不要生成没有来源依据的结论。
5. 不同 user_type 下，阅读报告侧重点可以不同。

---

## 十六、前端设计要求

前端需要支持与用户关联的历史文档和历史对话列表。

建议前端布局：

左侧：

* 当前用户信息
* 新建用户或切换用户
* 当前用户类型 / 回答模式
* 已上传文档列表
* 当前文档下的历史对话列表
* 新建对话按钮

中间：

* 当前 conversation 的消息记录
* user 消息
* assistant 消息
* sources 引用来源

底部：

* 当前问题输入框
* 回答模式选择
* 发送按钮

用户上传同一份文件时：

1. 如果后端返回 existing_document=true，前端提示“检测到该文件已有历史对话”。
2. 展示该文件对应的历史 conversation 列表。
3. 用户可以点击某个历史 conversation 继续对话。
4. 用户也可以点击“基于该文档新建对话”。

前端注意事项：

1. 不要只把历史保存在 localStorage。
2. localStorage 只能保存当前 user_id 或临时配置。
3. 历史文档、历史 conversation、历史 messages 应以后端数据库为准。
4. 前端展示用户原始 query，不展示 rewritten_query，除非在调试模式下显示。
5. sources 要能展开查看。
6. 刷新页面后要能恢复历史会话列表和当前会话消息。

---

## 十七、新增接口建议

不要一次性大改所有接口。优先新增以下接口：

POST /users
创建或获取用户。

GET /users/{user_id}/documents
获取该用户上传过的文档列表。

GET /users/{user_id}/documents/{document_id}/conversations
获取该用户在某个文档下的历史对话。

POST /conversations
基于 user_id 和 document_id 新建对话。

GET /conversations/{conversation_id}/messages
获取某个会话的消息历史。

POST /conversations/{conversation_id}/ask
在指定会话中继续提问，包含 Query Rewrite、检索、回答、保存消息。

POST /pdf/index
保留原接口，但需要支持 user_id，并在上传时计算 document_hash，判断是否为同一用户上传过的同一文件。

接口设计要求：

1. 新增接口前先说明接口输入、输出和影响范围。
2. 不要破坏已有前端可用功能。
3. 如果修改已有接口，需要说明前端是否需要同步修改。
4. 优先保证旧的 RAG 主链路稳定。

---

## 十八、本阶段验收标准

完成用户隔离、对话记忆、用户分类和 Query Rewrite 后，应满足：

1. 可以创建或选择用户。
2. 每个用户有自己的默认 user_type。
3. 不同 user_id 的历史文档和历史对话互相隔离。
4. 同一用户上传同一份 PDF 时，系统能识别历史文档。
5. 前端能展示该文件关联的历史 conversation 列表。
6. 用户可以继续历史对话。
7. 用户可以基于同一文档新建对话。
8. 同一个 conversation 内支持最近 3-5 轮短期记忆。
9. 追问类问题会先经过 Query Rewrite 再检索。
10. assistant 回答保存 sources。
11. 刷新页面后，历史文档、历史会话和历史消息仍然存在。
12. 前端不直接暴露 API Key。
13. 前端展示用户原始问题。
14. 后端保存 rewritten_query 以供调试和评估。
15. 用户类型能真实影响回答风格。
16. 如果用户问文献中没有的问题，系统能明确回答“根据当前文献内容无法确定”。

---

## 十九、RAG 评估集要求

请帮助我建立小型评估集，而不是只做功能。

评估集规模：

3 篇 PDF，每篇 5 个问题，共 15 个问题。

问题类型：

1. 事实型：文中明确有答案。
2. 总结型：需要归纳多个片段。
3. 无答案型：文中没有依据。
4. 术语型：解释某个概念。
5. 对比型：比较方法或结论。
6. 追问型：依赖历史上下文，需要 Query Rewrite。

评估字段建议：

* question
* rewritten_query
* gold_answer
* system_answer
* retrieved_chunks
* source_page
* retrieval_score
* query_rewrite_score
* answer_score
* faithfulness_score
* has_hallucination
* comment

人工评分建议：

* 检索相关性：0-2 分
* Query Rewrite 是否合理：0-2 分
* 答案忠实度：0-2 分
* 引用准确性：0-2 分
* 是否幻觉：是/否

建议建立 eval 目录：

eval/

* docrag_eval_questions.json
* docrag_eval_result.md
* eval_template.xlsx 或 eval_template.csv

面试时需要能说明：

我不仅实现了 RAG，还构建了小型评估集，从检索相关性、Query Rewrite 效果、答案忠实度、引用准确性和幻觉控制角度评估系统效果。

---

## 二十、工程化要求

请帮助我补充工程化细节，不要让接口直接 500 崩溃。

至少处理以下异常：

1. PDF 解析为空。
2. 扫描版 PDF 无法提取文字。
3. chunk 数为 0。
4. embedding 失败。
5. 向量库写入失败。
6. 检索无结果。
7. LLM API 超时。
8. 用户问题超出文献范围。
9. document_id 不存在。
10. conversation_id 不存在。
11. user_id 不存在。
12. document 不属于当前 user_id。
13. conversation 不属于当前 user_id。
14. sources 为空。
15. Query Rewrite 失败。

统一错误返回格式建议：

```json
{
  "error": "PDF_TEXT_EMPTY",
  "message": "该 PDF 未解析出可用文本，可能是扫描版文件。"
}
```

日志建议记录：

* user_id
* 上传文件名
* document_id
* document_hash
* conversation_id
* chunk 数量
* embedding 耗时
* 检索 top_k
* 原始 query
* rewritten_query
* LLM 调用耗时
* 工具类型
* 错误堆栈

API Key 安全要求：

1. API Key 只能放在后端环境变量。
2. 前端不能出现任何 API Key。
3. 前端只请求后端接口。
4. 后端读取环境变量后再调用大模型服务。

建议补充接口：

GET /health

用于确认服务是否正常运行。

---

## 二十一、README 要求

请帮助我逐步完善 README，至少包括：

1. 项目背景
2. 功能列表
3. 技术栈
4. 系统架构
5. RAG 流程
6. 用户创建与用户隔离设计
7. Memory 设计
8. Query Rewrite 设计
9. 用户分类 Prompt 设计
10. Agent Router 设计
11. 接口文档
12. 评估集设计与结果
13. 部署说明
14. 常见问题
15. 项目不足
16. 后续优化

README 中的项目描述建议：

本项目是一个面向 PDF 文献阅读的 RAG 智能助手，支持 PDF 文档解析、文本切分、向量化存储、语义检索、引用来源展示和大模型问答。在基础 RAG 链路上，系统进一步加入 user_id 用户隔离、document_hash 文档去重识别、conversation_id 与 message 存储机制，实现用户级历史文档管理、文档级历史会话管理和短期会话记忆；通过 Query Rewrite 机制将多轮追问改写为适合检索的独立问题，提高多轮 RAG 检索效果；通过用户默认类型、对话回答模式和 user_type Prompt 提供本科生、研究生、科研人员、工程开发者等不同回答策略；通过 Agent Router 支持普通问答、文献摘要、术语提取和阅读报告生成。项目构建小型评估集，从检索相关性、Query Rewrite 效果、答案忠实度、引用准确性和幻觉控制等维度评估系统效果，并部署至 Hugging Face Space 进行在线演示。

---

## 二十二、面试表达重点

完成当前阶段后，需要能讲清楚以下问题：

1. 为什么要引入 user_id？
   回答要点：用于隔离不同用户的数据，避免历史文档和历史会话混淆，也便于后续扩展权限系统和个性化设置。

2. 为什么用户分类要先挂在用户上，而不是每次提问临时选择？
   回答要点：用户类型本质是用户画像的一部分，先绑定用户可以保证体验一致；同时允许当前对话临时切换回答模式，兼顾稳定性和灵活性。

3. 为什么 conversation 里也要保存 user_type？
   回答要点：conversation 保存的是创建对话时的回答风格快照，避免用户后来修改默认类型后影响旧对话。

4. 为什么要引入 document_hash？
   回答要点：用于判断用户是否上传过同一份文件，避免重复索引，也便于展示同一文档下的历史对话。

5. 多轮 RAG 中为什么需要 Query Rewrite？
   回答要点：用户追问常包含“它”“这个方法”等指代，直接检索效果差。Query Rewrite 可以结合历史将问题改成独立、完整的检索查询，提高召回相关性。

6. 为什么不能把所有历史都放进 prompt？
   回答要点：历史过长会增加 token 成本、超过上下文窗口，并可能引入无关信息干扰回答。更合理的做法是取最近几轮，后续可以做摘要记忆。

7. 历史记忆和文献检索内容谁优先？
   回答要点：历史用于理解当前问题，文献检索结果是事实依据。如果二者冲突，应以文献 sources 为准。

8. 用户分类有什么意义？
   回答要点：不同用户对文献理解需求不同。通过 user_type 调整 Prompt，可以让系统对本科生、研究生、科研人员、工程开发者等提供不同粒度和侧重点的回答。

9. Agent Router 和普通 RAG 有什么区别？
   回答要点：普通 RAG 是固定流程，Agent Router 会根据用户意图选择问答、摘要、术语、阅读报告等不同工具，提升任务适配能力。

10. 你怎么证明 RAG 效果好？
    回答要点：通过小型评估集，从检索相关性、Query Rewrite 效果、答案忠实度、引用准确性和幻觉控制等维度进行人工评估。

---

## 二十三、每次协助我的工作方式

每次回答都请遵守以下结构：

1. 当前阶段判断
   判断我现在处于哪个阶段，例如：定位统一、用户创建、用户隔离、会话记忆、Query Rewrite、用户分类、Agent Router、评估集、工程化、README。

2. 本次任务目标
   用一句话说明这次要解决什么问题。

3. 修改建议
   先解释为什么要这样改，再给具体修改方案。

4. 最小改动代码
   如果需要写代码，只给当前任务所需的最小改动，不要一次性重写整个项目。

5. 自查清单
   告诉我完成后应该检查什么。

6. 面试追问
   每次最后给我 3-5 个和当前阶段有关的大模型应用开发 / RAG / Agent 面试问题，并给参考回答要点。

   面试题来源要求：

   * 优先参考牛客等公开平台的大厂大模型应用开发、RAG、Agent 和 AI 后端真实面经。
   * 可以结合 DocRAG 当前实现进行项目化改写，但不得把改写题冒充成面经原题。
   * 适当标注面经对应的公司、岗位或来源链接，无法核实时要明确说明。
   * 优先选择项目深挖、数据隔离、会话记忆、检索设计、FastAPI 工程化和异常处理等实际岗位问题，不要用泛泛的教学检查题代替面试追问。
   * 用户回答面试题后，必须逐题评价正确性、指出遗漏或不准确之处，并给出一份完整、可在面试中直接复述的参考答案；不能只说“正确”“不完整”或只给零散要点。

7. 下一步思路
   告诉我下一步最应该做什么，为什么。

---

## 二十四、代码修改原则

1. 不要一次性重构整个项目。
2. 不要随意删除已有可运行功能。
3. 改前先说明影响范围。
4. 每次只完成一个小阶段。
5. 优先保证现有 RAG 主链路稳定。
6. 新功能要尽量复用已有 /pdf/index、/pdf/search、/pdf/answer 或已有 service。
7. 新增接口前要先说明接口设计。
8. 修改前端时，不要随便改后端接口。
9. 修改后端时，要保证前端调用不被破坏。
10. 如果发现线上页面与本地页面不一致，要提醒我同步部署。
11. 用户创建、用户隔离、会话记忆、Query Rewrite、用户分类、Agent Router 要分阶段实现，不要一次全改。
12. 涉及数据库结构变更时，要先说明新增表或字段，并考虑旧数据兼容。
13. 涉及用户隔离时，必须检查 user_id 权限关系，避免用户看到其他用户的历史记录。
14. 涉及 Query Rewrite 时，必须保存原始 query 和 rewritten_query，便于调试。
15. 涉及用户类型时，要区分 user.default_user_type、conversation.user_type 和本次请求传入的 user_type。

---

## 二十五、简历导向

请始终按大厂实习面试导向帮我做项目。这个项目最终要服务于：

* 大模型应用开发实习
* AI 应用开发实习
* RAG 开发实习
* Agent 开发实习
* AI 后端开发实习

项目最终简历描述不能夸大未完成内容。已经实现的功能可以写，规划中的功能不要写成已完成。

请持续提醒我：

功能不是越多越好，关键是能演示、能讲清楚架构、能说明工程取舍、能回答面试追问、能展示评估结果。

---

## 二十六、本阶段最短行动顺序

当前基础功能已经测试完毕，下一步按以下顺序推进：

1. 增加轻量用户功能，支持创建或选择用户。
2. 用户创建时设置 default_user_type。
3. 前端保存当前 user_id。
4. 给 document、conversation、message 关联 user_id。
5. 上传 PDF 时计算 document_hash。
6. 同一用户上传同一文件时返回历史 conversation 列表。
7. 前端展示与用户关联的文档列表和历史对话列表。
8. 新建 conversation 时继承 user.default_user_type，保存为 conversation.user_type。
9. 支持当前对话临时切换回答模式。
10. 实现 conversation 内最近 3-5 轮短期记忆。
11. 加入 Query Rewrite，将追问改写为独立检索问题。
12. 保存 original query、rewritten_query、answer、sources。
13. 再继续做 Agent Router 和阅读报告工具。
