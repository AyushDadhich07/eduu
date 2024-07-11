import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from text_processing import process_pdf, chunk_text
from embeddings import get_embeddings, search_similar_chunks
from summarization import summarize_document, summarize_section
from qa_generation import generate_qa_pairs
from question_paper_generator import generate_question_paper
# import ollama
# from ollama.models import Mistral
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from gtts import gTTS
from study_plan_generator import generate_study_plan
from playsound import playsound


def playaudio(audio):
    playsound(audio)
# Initialize models and database
@st.cache_resource
def initialize_resources():
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.Client()
    try:
        collection = chroma_client.get_collection("pdf_collection")
    except ValueError:
        collection = chroma_client.create_collection("pdf_collection")
    
    llm = Ollama(model="mistral")
    # tokenizer = AutoTokenizer.from_pretrained("gpt2")  #mistralai/Mixtral-8x7B-Instruct-v0.1
    # model = AutoModelForCausalLM.from_pretrained("gpt2")
    # generation_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    return embedding_model, collection,llm

embedding_model, collection,llm = initialize_resources()

st.title("PDF Learning Assistant")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    text = process_pdf(pdf_reader)
    chunks = chunk_text(text)
    
    embeddings = get_embeddings(chunks, embedding_model)
    
    # Clear existing data in the collection
    collection.delete()
    
    # Store embeddings in Chroma
    try:
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
        st.success("PDF processed and stored successfully!")
    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {str(e)}")

question = st.text_input("Ask a question about the PDF:")

if question:
    try:
        relevant_chunks = search_similar_chunks(question, embedding_model, collection)
        context = " ".join(relevant_chunks)
        # print(context)
        prompt = f"""Based on the following context from a textbook chapter, provide a detailed and comprehensive answer to the question. Your answer should be suitable for a school assignment, demonstrating thorough understanding and covering multiple aspects of the topic.

        Context: {context}

        Question: {question}

        Detailed Answer:"""
        
        # Generate a comprehensive answer
        # llm.complete("Who is Laurie Voss? write in 10 words")
        response = llm.complete(prompt)
        # response = generation_pipeline(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
        
        # Extract the generated answer (remove the prompt)
        # answer = response.split("Detailed Answer:")[-1].strip()
        answer = response
        
        st.write("Answer:", answer)
    except Exception as e:
        st.error(f"An error occurred while answering the question: {str(e)}")


st.header("Tutor")
summarize_option = st.radio("Choose tutor option:", ["Whole Document", "Section by Keywords"])

if summarize_option == "Whole Document":
    if st.button("Teach Whole Document"):
        summary = summarize_document(text, llm)
        st.write("Summary:", summary)
        tts = gTTS(text=str(summary), lang='en', tld='com')
        tts.save("answer.mp3")
        # Play the audio
        audio_file = open("answer.mp3", "rb")
        # playaudio("textaud.mp3")
        st.audio(audio_file, format="audio/mp3", start_time=0)
else:
    keywords = st.text_input("Enter keywords for learning about a section:")
    if keywords and st.button("Teach Section"):
        summary = summarize_section(text, keywords, embedding_model, collection, llm)
        st.write("Section Summary:", summary)
        tts = gTTS(text=str(summary), lang='en', tld='com')
        tts.save("answer.mp3")
        # Play the audio
        # audio_file = open("answer.mp3", "rb")
        # playaudio("answer.mp3")
        # st.audio(audio_file, format="audio/mp3", start_time=0)

# Question-Answer Generation Section
st.header("Generate Study Questions")
num_questions = st.slider("Number of questions to generate:", 1, 10, 5)

if st.button("Generate Questions"):
    qa_pairs = generate_qa_pairs(text, num_questions, llm)
    for i, (q, a) in enumerate(qa_pairs, 1):
        st.write(f"Question {i}: {q}")
        with st.expander("Show Answer"):
            st.write(a)

# New section for Question Paper Generation
st.header("Generate Question Paper")
num_questions_paper = st.slider("Number of questions in the paper:", 10, 50, 20)
previous_paper = st.file_uploader("Upload previous year's paper (optional)", type="pdf")

if st.button("Generate Question Paper"):
    previous_paper_text = None
    if previous_paper:
        previous_pdf_reader = PdfReader(previous_paper)
        previous_paper_text = process_pdf(previous_pdf_reader)
    
    question_paper = generate_question_paper(text, llm, num_questions_paper, previous_paper_text)
    
    st.subheader("Generated Question Paper")
    for i, question in enumerate(question_paper, 1):
        st.write(f"Question {i}: {question['question']}")
        if question['type'] == "MCQ":
            for j, option in enumerate(question['options'], 1):
                st.write(f"  {j}. {option}")
        with st.expander("Show Answer"):
            st.write(question['answer'] if question['type'] != "MCQ" else question['correct_answer'])


#
# Updated section for Study Plan Generation
st.header("Generate Study Plan")
duration_days = st.slider("Study plan duration (days):", 1, 5, 3)

if st.button("Generate Study Plan"):
    study_plan = generate_study_plan(text, llm, duration_days)
    
    st.subheader("Your Personalized Study Plan")
    for day, activities in study_plan.items():
        st.write(f"**{day}**")
        for activity in activities:
            if "topic" in activity:
                st.write(f"### {activity['topic']}")
                st.write(activity['content'])
            elif "review" in activity:
                st.write("### Review Session")
                st.write(f"Review the following topics: {', '.join(activity['review'])}")
        st.write("---")