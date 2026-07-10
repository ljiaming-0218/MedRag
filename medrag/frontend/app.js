let currentDocumentId = "";
let currentConversationId = "";

function getApiBase() {
  return window.location.origin;
}

function setStatus(id, message, type = "info") {
  const box = document.getElementById(id);
  box.textContent = message;
  box.className = `status show ${type}`;
}

function clearStatus(id) {
  const box = document.getElementById(id);
  box.textContent = "";
  box.className = "status";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function parseResponse(response) {
  const text = await response.text();
  let data;

  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { detail: text || "响应不是 JSON 格式" };
  }

  if (!response.ok) {
    const message = data.detail || data.message || `请求失败，状态码：${response.status}`;
    throw new Error(message);
  }

  return data;
}

function buildUrl(path, params) {
  const url = new URL(`${getApiBase()}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, value);
  });
  return url;
}

async function createConversation(userId, documentId, title) {
  const response = await fetch(`${getApiBase()}/conversations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      document_id: documentId,
      title,
    }),
  });
  return parseResponse(response);
}

async function startNewConversation() {
  if (!currentDocumentId) {
    setStatus("answerStatus", "请先上传并索引一个 PDF 文件。", "error");
    return;
  }

  try {
    const file = document.getElementById("pdfFile").files[0];
    const title = file ? file.name.replace(/\.pdf$/i, "") : "新会话";
    const userId = document.getElementById("userId").value.trim();
    const conversation = await createConversation(userId, currentDocumentId, title);
    currentConversationId = conversation.conversation_id;
    document.getElementById("answerConversationId").value = currentConversationId;
    document.getElementById("answerResult").innerHTML = "";
    document.getElementById("answerQuery").value = "";
    setStatus("answerStatus", "已创建新会话，可以开始提问。", "success");
    document.getElementById("answerQuery").focus();
  } catch (error) {
    setStatus("answerStatus", error.message, "error");
  }
}

function scrollChatToBottom() {
  const chatWindow = document.getElementById("chatWindow");
  requestAnimationFrame(() => {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  });
}

function renderMeta(targetId, data) {
  const target = document.getElementById(targetId);
  target.innerHTML = `
    <div class="meta">
      <div class="meta-item">
        <span>文件名</span>
        <strong>${escapeHtml(data["文件名"])}</strong>
      </div>
      <div class="meta-item">
        <span>document_id</span>
        <strong>${escapeHtml(data.document_id)}</strong>
      </div>
      <div class="meta-item">
        <span>总页数</span>
        <strong>${escapeHtml(data["总页数"])}</strong>
      </div>
      <div class="meta-item">
        <span>文本块</span>
        <strong>${escapeHtml(data["成功保存块数"])} / ${escapeHtml(data["总块数"])}</strong>
      </div>
    </div>
  `;
}

function renderSearchResults(targetId, chunks) {
  const target = document.getElementById(targetId);

  if (!chunks || chunks.length === 0) {
    target.innerHTML = '<p class="hint">没有检索到相关内容。</p>';
    return;
  }

  target.innerHTML = chunks
    .map((chunk, index) => {
      const meta = chunk["元数据"] || {};
      const distance = typeof chunk["距离"] === "number" ? chunk["距离"].toFixed(4) : chunk["距离"];
      return `
        <div class="chunk">
          <div class="chunk-title">
            <span>结果 ${index + 1} · 第 ${escapeHtml(meta.page_number ?? "-")} 页 · 块 ${escapeHtml(meta.chunk_index ?? "-")}</span>
            <span>距离：${escapeHtml(distance ?? "-")}</span>
          </div>
          <p>${escapeHtml(chunk["文本块"])}</p>
        </div>
      `;
    })
    .join("");
}

async function indexPdf() {
  const userId = document.getElementById("userId").value.trim();
  const fileInput = document.getElementById("pdfFile");
  const chunkSize = document.getElementById("chunkSize").value;
  const chunkOverlap = document.getElementById("chunkOverlap").value;
  const button = document.getElementById("indexButton");

  if (!fileInput.files.length) {
    setStatus("indexStatus", "请先选择一个 PDF 文件。", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  clearStatus("indexStatus");
  document.getElementById("indexResult").innerHTML = "";
  button.disabled = true;
  setStatus("indexStatus", "正在索引 PDF，embedding 可能需要一点时间...", "info");

  try {
    const url = buildUrl("/pdf/index", {
      user_id: userId,
      chunk_size: chunkSize,
      chunk_overlap: chunkOverlap,
    });
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });
    const data = await parseResponse(response);

    currentDocumentId = data.document_id || "";
    document.getElementById("searchDocumentId").value = currentDocumentId;

    const title = fileInput.files[0].name.replace(/\.pdf$/i, "");
    const conversation = await createConversation(userId, currentDocumentId, title);
    currentConversationId = conversation.conversation_id;
    document.getElementById("answerConversationId").value = currentConversationId;

    setStatus("indexStatus", `${data.message || "PDF 索引完成。"} 已创建问答会话。`, "success");
    renderMeta("indexResult", data);
    document.getElementById("answerResult").innerHTML = "";
  } catch (error) {
    setStatus("indexStatus", error.message, "error");
  } finally {
    button.disabled = false;
  }
}

async function searchChunks() {
  const userId = document.getElementById("userId").value.trim();
  const documentId = document.getElementById("searchDocumentId").value.trim();
  const query = document.getElementById("searchQuery").value.trim();
  const topK = document.getElementById("searchTopK").value;
  const button = document.getElementById("searchButton");

  if (!documentId || !query) {
    setStatus("searchStatus", "请填写 document_id 和问题。", "error");
    return;
  }

  clearStatus("searchStatus");
  document.getElementById("searchResult").innerHTML = "";
  button.disabled = true;
  setStatus("searchStatus", "正在检索相关文本块...", "info");

  try {
    const url = buildUrl("/pdf/search", {
      document_id: documentId,
      user_id: userId,
      query,
      n_results: topK,
    });
    const response = await fetch(url, { method: "POST" });
    const data = await parseResponse(response);

    setStatus("searchStatus", `检索完成，共找到 ${data["检索到的相关内容数"]} 条相关内容。`, "success");
    renderSearchResults("searchResult", data["相关内容"]);
  } catch (error) {
    setStatus("searchStatus", error.message, "error");
  } finally {
    button.disabled = false;
  }
}

async function answerQuestion() {
  const conversationId = document.getElementById("answerConversationId").value.trim();
  const query = document.getElementById("answerQuery").value.trim();
  const topK = Number(document.getElementById("answerTopK").value);
  const button = document.getElementById("answerButton");
  const userId = document.getElementById("userId").value.trim();
  if (!conversationId || !query || !userId) {
    setStatus("answerStatus", "请先建立 PDF 索引并输入问题和用户 ID。", "error");
    return;
  }

  clearStatus("answerStatus");
  button.disabled = true;
  setStatus("answerStatus", "正在生成回答...", "info");

  try {
    const response = await fetch(`${getApiBase()}/conversations/${encodeURIComponent(conversationId)}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        query,
        history_limit: 6,
        n_results: topK,
      }),
    });
    const data = await parseResponse(response);
    const sourceTargetId = `answerChunks-${String(data.assistant_message?.message_id || Date.now()).replace(/[^a-zA-Z0-9_-]/g, "")}`;

    setStatus("answerStatus", "回答生成完成。", "success");
    document.getElementById("answerResult").insertAdjacentHTML("beforeend", `
      <div class="message">
        <div class="avatar user">你</div>
        <div class="message-content">
          <div class="message-role">User</div>
          <p>${escapeHtml(query)}</p>
        </div>
      </div>

      <div class="message">
        <div class="avatar assistant">AI</div>
        <div class="message-content">
          <div class="message-role">DocRAG Assistant</div>
          <p>${escapeHtml(data.answer)}</p>
          <div class="sources-title">引用来源 · ${escapeHtml(data.sources?.length ?? 0)} 条</div>
          <div id="${sourceTargetId}"></div>
        </div>
      </div>
    `);
    renderSearchResults(sourceTargetId, data.sources);
    document.getElementById("answerQuery").value = "";
    scrollChatToBottom();
  } catch (error) {
    setStatus("answerStatus", error.message, "error");
  } finally {
    button.disabled = false;
  }
}

document.getElementById("answerQuery").addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    answerQuestion();
  }
});
