from collections import defaultdict
import math

def generate_study_plan(text, llm, duration_days=7):
    # Extract topics from the text
    topics = extract_topics(text, llm)
    
    # Generate a study plan
    study_plan = create_dynamic_study_plan(llm, topics, duration_days)
    
    return study_plan

def extract_topics(text, llm):
    prompt = f"""Extract the main topics from the following text. Each topic should be a key concept or subject area covered in the material. List the topics in order of importance or prominence in the text.

    Text: {text[:4000]}  

    Topics:
    1.
    2.
    3.
    ..."""

    response = llm.complete(prompt)
    topics = [topic.strip() for topic in str(response).split('\n') if topic.strip()]
    return topics[:10]  # Limit to top 10 topics

def create_dynamic_study_plan(llm, topics, duration_days):
    study_plan = defaultdict(list)
    
    # Calculate topics per day
    topics_per_day = math.ceil(len(topics) / duration_days)
    
    for day in range(1, duration_days + 1):
        start_index = (day - 1) * topics_per_day
        end_index = min(day * topics_per_day, len(topics))
        day_topics = topics[start_index:end_index]
        
        for topic in day_topics:
            study_content = generate_study_content(topic, llm)
            study_plan[f"Day {day}"].append({"topic": topic, "content": study_content})
        
        # Add a review session if it's not the first day and there are previous topics
        if day > 1:
            review_topics = topics[:start_index]
            study_plan[f"Day {day}"].append({"review": review_topics})
    
    return dict(study_plan)

def generate_study_content(topic, llm):
    prompt = f"""Create a structured, concise study guide for a school student on the following topic. 
    The content should be informative and designed to help the student ace a test on this subject. 
    Include key points, definitions, and examples where appropriate. 
    Format the content with clear headings and bullet points for easy reading.

    Topic: {topic}

    Study Guide:"""

    response = llm.complete(prompt)
    return str(response).strip()