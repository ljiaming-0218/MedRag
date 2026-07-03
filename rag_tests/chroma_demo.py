from pathlib import Path
import sys

import chromadb


# 把项目后端目录加入 Python 的导入路径，方便复用 Embedding 函数。
BACKEND_DIR = Path(__file__).resolve().parents[1] / "medrag" / "backend"
sys.path.append(str(BACKEND_DIR))

from services.embedding_service import get_embedding, get_embeddings


CHROMA_DATA_DIR = Path(__file__).resolve().parent / "chroma_data"
COLLECTION_NAME = "medical_chunks_test"


def main() -> None:
    query = "阿司匹林的作用是什么？"
    query_embedding = get_embedding(query)
    documents = [
        "阿司匹林可以缓解疼痛。",
        "今天的天气很好。",
    ]

    ids = ["chunk_1", "chunk_2"]

    metadatas = [
        {"page_number": 1, "chunk_index": 1},
        {"page_number": 2, "chunk_index": 2},
    ]

    embeddings = get_embeddings(documents)

    client = chromadb.PersistentClient(path=str(CHROMA_DATA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    result = collection.query(
    query_embeddings=[query_embedding],
    n_results=1,
)

    print(result)

    
if __name__ == "__main__":
    main()
