from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def main() -> None:
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5", local_files_only=True)

    query = ["阿司匹林有什么作用？",
             "布洛芬和阿司匹林有什么区别？",
]
    sentences = [
        "阿司匹林可以缓解疼痛，也可以抑制血小板聚集。",
        "布洛芬是一种常见的解热镇痛药。",
        "今天北京天气很好，适合出门散步。",
    ]

    query_vector = model.encode(query)
    sentence_vectors = model.encode(sentences)

    scores = cosine_similarity(query_vector, sentence_vectors)[0]
    results = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)
    for sentence, score in results:
        print(f"相似度: {score:.4f}")
        print(f"文本: {sentence}")
        print()


if __name__ == "__main__":
    main()
