from pathlib import Path

import fitz


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {path}")

    pages = []
    with fitz.open(path) as document:
        for index, page in enumerate(document, start=1):
            text = page.get_text("text").strip()
            pages.append(
                {
                    "页码": index,
                    "文本": text,
                }
            )

    return pages


def extract_pdf_text(pdf_path: str | Path) -> str:
    pages = extract_pdf_pages(pdf_path)
    return "\n\n".join(
        f"[第 {item['页码']} 页]\n{item['文本']}" for item in pages if item["文本"]
    )
