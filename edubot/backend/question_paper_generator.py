import random
from qa_generation import generate_qa_pairs
import re
from collections import Counter

def generate_question_paper(text, llm, num_questions, previous_paper=None):
    sections = {
        "Multiple Choice": 0.3,
        "Short Answer": 0.4,
        "Long Answer": 0.3
    }
    
    question_paper = []
    
    for section, proportion in sections.items():
        section_questions = int(num_questions * proportion)
        qa_pairs = generate_qa_pairs(text, section_questions, llm)
        
        for q, a in qa_pairs:
            if section == "Multiple Choice":
                options = generate_options(q, a, text, llm)
                question_paper.append({
                    "type": "MCQ",
                    "question": q,
                    "options": options,
                    "correct_answer": a
                })
            else:
                question_paper.append({
                    "type": section,
                    "question": q,
                    "answer": a
                })
    
    if previous_paper:
        question_paper = adapt_to_previous_paper(question_paper, previous_paper)
    
    return question_paper

def generate_options(question, correct_answer, context, llm):
    prompt = f"""Generate 3 plausible but incorrect options for the following question and answer:
    Question: {question}
    Correct Answer: {correct_answer}
    Context: {context}
    
    Incorrect Options:
    1.
    2.
    3."""
    
    response = llm.complete(prompt)
    incorrect_options = [option.strip() for option in str(response).split('\n') if option.strip()]
    
    options = incorrect_options + [correct_answer]
    random.shuffle(options)
    return options

def adapt_to_previous_paper(current_paper, previous_paper_text):
    # Analyze the structure of the previous paper
    previous_structure = analyze_paper_structure(previous_paper_text)
    
    # Adjust the current paper based on the previous paper's structure
    adjusted_paper = []
    
    # Distribute questions according to the previous paper's section distribution
    section_distribution = previous_structure['section_distribution']
    total_questions = len(current_paper)
    
    for section, proportion in section_distribution.items():
        section_questions = int(total_questions * proportion)
        section_questions = max(section_questions, 1)  # Ensure at least one question per section
        
        # Filter questions of the current type
        available_questions = [q for q in current_paper if q['type'] == section]
        
        # If we don't have enough questions of this type, we'll need to generate more or adjust
        if len(available_questions) < section_questions:
            # For simplicity, we'll just use what we have and note the discrepancy
            adjusted_paper.extend(available_questions)
            print(f"Warning: Not enough {section} questions available. Used {len(available_questions)} instead of {section_questions}.")
        else:
            adjusted_paper.extend(available_questions[:section_questions])
    
    # Adjust difficulty based on previous paper
    adjust_difficulty(adjusted_paper, previous_structure['difficulty_level'])
    
    # Apply formatting similar to the previous paper
    apply_formatting(adjusted_paper, previous_structure['formatting'])
    
    return adjusted_paper

def analyze_paper_structure(paper_text):
    structure = {
        'section_distribution': {},
        'difficulty_level': 'medium',
        'formatting': {}
    }
    
    # Analyze section distribution
    sections = ['Multiple Choice', 'Short Answer', 'Long Answer']
    section_counts = {section: len(re.findall(rf"{section}.*?question", paper_text, re.IGNORECASE)) for section in sections}
    total_questions = sum(section_counts.values())
    structure['section_distribution'] = {section: count/total_questions for section, count in section_counts.items() if count > 0}
    
    # Analyze difficulty level
    difficulty_keywords = {
        'easy': ['basic', 'simple', 'straightforward'],
        'medium': ['analyze', 'explain', 'describe'],
        'hard': ['evaluate', 'criticize', 'synthesize']
    }
    difficulty_counts = {level: sum(paper_text.lower().count(word) for word in words) 
                         for level, words in difficulty_keywords.items()}
    structure['difficulty_level'] = max(difficulty_counts, key=difficulty_counts.get)
    
    # Analyze formatting
    structure['formatting']['numbering_style'] = 'numeric' if re.search(r'\d+\.\s', paper_text) else 'roman'
    structure['formatting']['has_sections'] = bool(re.search(r'section [a-z]', paper_text, re.IGNORECASE))
    
    return structure

def adjust_difficulty(paper, target_difficulty):
    difficulty_adjustments = {
        'easy': lambda q: q.replace('explain', 'describe').replace('analyze', 'list'),
        'hard': lambda q: q.replace('describe', 'analyze').replace('list', 'evaluate')
    }
    
    if target_difficulty in difficulty_adjustments:
        for question in paper:
            question['question'] = difficulty_adjustments[target_difficulty](question['question'])

def apply_formatting(paper, formatting):
    if formatting['numbering_style'] == 'roman':
        roman_numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
        for i, question in enumerate(paper):
            question['number'] = roman_numerals[i] if i < len(roman_numerals) else str(i + 1)
    else:
        for i, question in enumerate(paper):
            question['number'] = str(i + 1)
    
    if formatting['has_sections']:
        current_section = 'A'
        for question in paper:
            question['section'] = current_section
            if question['type'] != paper[paper.index(question) - 1]['type']:
                current_section = chr(ord(current_section) + 1)

# Helper function to generate more questions if needed
def generate_more_questions(text, llm, question_type, num_questions):
    # This function would use the existing question generation logic to create more questions of a specific type
    # For now, we'll leave it as a placeholder
    pass