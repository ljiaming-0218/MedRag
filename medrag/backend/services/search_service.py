

from services.rerank_service import rerank_chunks
from services.embedding_service import get_embedding
from services.vector_store_service import query_chunks


def search_relevant_chunks(document_id: str, query: str, n_results: int = 3) -> list[dict]:
    if not query.strip():
        raise ValueError("查询内容不能为空")
    if n_results <= 0:
        raise ValueError("n_results 必须大于 0")
    if not document_id.strip():
        raise ValueError("document_id 不能为空")



    query_embedding = get_embedding(query)
    search_results = query_chunks(document_id, query_embedding, n_results*5)
    results = []
    
    for doc, score, metadata in zip(search_results["documents"][0],
                                        search_results["distances"][0],
                                        search_results["metadatas"][0]): 
        if is_summary_question(query) and metadata["page_number"] > 2:
                continue

        if not is_useful_chunk(doc):
                continue
        results.append({
                "文本块": doc,
                "距离": score,
                "元数据": metadata
            })
        
    if not results:
        return []
    result = rerank_chunks(query, results, n_results)


    return result   



def is_useful_chunk(text: str) -> bool:
    useless_keywords = ["creative commons","reprints and permissions","publisher’s note","copyright","license"]
    lower_text = text.lower()
    return not any(keyword in lower_text for keyword in useless_keywords)

def is_summary_question(query: str) -> bool:
    summary_keywords = ["核心观点是什么","这篇文章讲了什么","总结一下","主要内容是什么","文章核心观点是什么","主要研究什么","这篇论文讲了什么"]
    return  any(keyword in query for keyword in summary_keywords)