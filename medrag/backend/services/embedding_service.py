from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
model = SentenceTransformer(MODEL_NAME, local_files_only=True)

def get_embedding(text: str) -> list[float]:
    
    sentence_vector = model.encode([text])[0]
    return sentence_vector.tolist()




def get_embeddings(texts: list[str]) -> list[list[float]]:
    sentence_vectors = model.encode(texts)
    return sentence_vectors.tolist()

def embed_chunks(chunks):
    texts = [chunk["文本块"] for chunk in chunks]
    sentence_vectors = get_embeddings(texts)
    for chunk, vector in zip(chunks, sentence_vectors):
        chunk["embedding"] = vector
    return chunks