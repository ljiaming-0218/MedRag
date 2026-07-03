from sentence_transformers import CrossEncoder

reranker_model  = CrossEncoder("BAAI/bge-reranker-base")

def rerank_chunks(query: str, chunks: list[dict], top_k: int) -> list[dict]:
    if not query.strip():
        raise ValueError("查询内容不能为空")
    if top_k <= 0:
        raise ValueError("top_k 必须大于 0")
    if not chunks:
        raise ValueError("chunks 不能为空")
    

    pairs = []
    for chunk in chunks:
        pairs.append([query,chunk["文本块"]])
        
    
    scores = reranker_model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    return sorted(
                    chunks,
                    key=lambda x: x["rerank_score"],
                    reverse=True
                )[:top_k]

    