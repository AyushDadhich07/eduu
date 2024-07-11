def generate_qa_pairs(text, num_questions, llm, chunk_size=2000, overlap=200):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]
    qa_pairs = []

    for chunk in chunks:
        prompt = f"""Generate {num_questions // len(chunks) + 1} a question-answer pair based on the following text. Each question should test understanding of key concepts, and the answer should be comprehensive.

        {chunk}

        Format each pair as:
        Q: [Question]
        A: [Answer]

        Question-Answer Pairs:"""
        
        response = llm.complete(prompt)
        chunk_qa_pairs = parse_qa_pairs(response)
        qa_pairs.extend(chunk_qa_pairs)
    
    return qa_pairs[:num_questions]

def parse_qa_pairs(response):
    pairs = []
    response = str(response)
    lines = response.strip().split('\n')
    current_question = None
    current_answer = []

    for line in lines:
        if line.startswith('Q:'):
            if current_question:
                pairs.append((current_question, ' '.join(current_answer)))
            current_question = line[2:].strip()
            current_answer = []
        elif line.startswith('A:'):
            current_answer.append(line[2:].strip())
        elif current_question:
            current_answer.append(line.strip())

    if current_question:
        pairs.append((current_question, ' '.join(current_answer)))

    return pairs