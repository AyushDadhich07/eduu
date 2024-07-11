import numpy as np

def get_embeddings(chunks, model):
    embeddings = model.encode(chunks)
    return embeddings.tolist()  # Convert NumPy array to list of lists

def search_similar_chunks(query, model, collection, top_k=5):
    query_embedding = model.encode([query])[0].tolist()  # Convert to list
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

def find_relevant_chunks(keywords, model, collection, top_k=3):
    keyword_embedding = model.encode([keywords])[0].tolist()
    results = collection.query(
        query_embeddings=[keyword_embedding],
        n_results=top_k
    )
    return results['documents'][0]