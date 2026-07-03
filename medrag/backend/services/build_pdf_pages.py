from fastapi import FastAPI, File, HTTPException, UploadFile
from services.pdf_service import extract_pdf_pages
from services.pdf_upload import upload_pdf
from pathlib import Path



async def build_pdf_pages(file: UploadFile) -> dict:
    file = await upload_pdf(file)  # 调用上传函数，确保文件已保存
    safe_name = file["文件名"]
    save_path = Path(file["保存路径"])
    document_id = file["document_id"]
    try:
        pages = extract_pdf_pages(save_path) 
        for page in pages:
            page["document_id"] = document_id  
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF 解析失败: {exc}") from exc
    
    return {
        "文件名": safe_name,
        "总页数": len(pages),
        "每页内容": pages,
        "document_id": document_id
    }