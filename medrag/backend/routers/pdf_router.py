from fastapi import APIRouter, File, HTTPException, UploadFile

from services.validation_service import validate_chunk_params
from services.llm_service import generate_answer
from services.prompt_service import build_rag_prompt
from services.text_splitter import split_pages
from services.embedding_service import embed_chunks
from services.vector_store_service import save_chunks
from services.build_pdf_pages import build_pdf_pages
from services.search_service import search_relevant_chunks

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"],
)


def raise_service_error(error: Exception) -> None:
    status_code = 400 if isinstance(error, ValueError) else 500
    raise HTTPException(status_code=status_code, detail=str(error)) from error


@router.post("/search")
async def search_pdf(document_id: str, query: str, n_results: int = 3) -> dict:
    try:
        results = search_relevant_chunks(document_id, query, n_results)
    except (ValueError, RuntimeError) as e:
        raise_service_error(e)

    return {
        "查询": query,
        "检索到的相关内容数": len(results),
        "相关内容": results,
        "query": query,
        "sources_count": len(results),
        "sources": results
    }

@router.post("/index")
async def index_pdfs(file: UploadFile = File(...), chunk_size: int = 500, chunk_overlap: int = 50) -> dict:
    
    try:
        validate_chunk_params(chunk_size, chunk_overlap)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    context = await build_pdf_pages(file)  # 调用上传函数，确保文件已保存
    chunks = split_pages(context["每页内容"], chunk_size, chunk_overlap)
    embedded_chunks = embed_chunks(chunks)
    try:
        saved_count = save_chunks(embedded_chunks)
    except RuntimeError as e:
        raise_service_error(e)
    
    return {
        "message": f"成功处理文件 '{context['文件名']}'，共 {context['总页数']} 页，生成 {len(chunks)} 个文本块，成功保存 {saved_count} 个块到向量数据库。",
        "文件名": context["文件名"],
        "总页数": context["总页数"],
        "总块数": len(chunks),
        "成功保存块数": saved_count,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "document_id": context["document_id"]
    }

@router.post("/parse")
async def parse_pdf(file: UploadFile = File(...)) -> dict:
    return await build_pdf_pages(file)

@router.post("/chunks")
async def parse_pdf_chunks(file: UploadFile = File(...), chunk_size: int = 500, chunk_overlap: int = 50) -> dict:
    try:
        validate_chunk_params(chunk_size, chunk_overlap)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    context = await build_pdf_pages(file)  # 调用上传函数，确保文件已保存

    chunks = split_pages(context["每页内容"], chunk_size, chunk_overlap)

    return {
        "文件名": context["文件名"],
        "总页数": context["总页数"],
        "每页内容块": chunks,
        "document_id": context["document_id"]
    }

@router.post("/prompt-preview")
async def preview_rag_prompt(document_id: str, query: str, n_results: int = 3) -> dict:
    try:
        retrieved_chunks = search_relevant_chunks(document_id, query, n_results)
    except (ValueError, RuntimeError) as e:
        raise_service_error(e)

    prompt = build_rag_prompt(query, retrieved_chunks)

    return {
        "查询": query,
        "生成的提示": prompt,
        "检索到的相关内容数": len(retrieved_chunks),
        "相关内容": retrieved_chunks,
        "query": query,
        "prompt": prompt,
        "sources_count": len(retrieved_chunks),
        "sources": retrieved_chunks
    }

@router.post("/answer")
def answer_pdf_question(document_id: str, query: str, n_results: int = 3) -> dict:
    try:
        retrieved_chunks = search_relevant_chunks(document_id, query, n_results)
    except (ValueError, RuntimeError) as e:
        raise_service_error(e)

    prompt = build_rag_prompt(query, retrieved_chunks)
    answer = generate_answer(prompt)

    return {
        "查询": query,
        "生成的答案": answer,
        "检索到的相关内容数": len(retrieved_chunks),
        "相关内容": retrieved_chunks,
        "query": query,
        "answer": answer,
        "sources_count": len(retrieved_chunks),
        "sources": retrieved_chunks
    }
