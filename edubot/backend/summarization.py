from embeddings import search_similar_chunks

def summarize_document(text, llm, chunk_size=1000, overlap=200):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]
    summaries = []

    for chunk in chunks:
        prompt = f"""You are a tutor, Teach me the following text in a concise manner but explaining the concept, capturing the main points and key information, give examples wherever necessary:

        {chunk}

        Summary:"""
        
        summary = str(llm.complete(prompt))
        summaries.append(summary)
    
    final_summary_prompt = f"""You are a tutor, Combine the following teachings into a coherent, comprehensive and structured way:

    {' '.join(summaries)}

    Final Output to be learnt by a school going child:"""
    
    final_summary = llm.complete(final_summary_prompt)
    return final_summary

def summarize_section(text, keywords, embedding_model, collection, llm):
    relevant_chunks = search_similar_chunks(keywords, embedding_model, collection, top_k=3)
    context = " ".join(relevant_chunks)
    
    prompt = f"""Teach me the following text, I am a school student looking to ace the test, you can give relevant and easy to understand examples as well to explain, focusing on the aspects related to these keywords: {keywords}

    {context}

    Summary:"""
    
    summary = llm.complete(prompt)
    return summary