from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import PDFUploadSerializer, ProcessedPDFSerializer
from .models import ProcessedPDF
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from llama_index.llms.ollama import Ollama
from text_processing import process_pdf, chunk_text
from embeddings import get_embeddings, search_similar_chunks
from summarization import summarize_document, summarize_section
from qa_generation import generate_qa_pairs
from question_paper_generator import generate_question_paper
from study_plan_generator import generate_study_plan

class PDFProcessView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            pdf_reader = PdfReader(pdf_file)
            text = process_pdf(pdf_reader)
            chunks = chunk_text(text)
            
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            chroma_client = chromadb.Client()
            collection = chroma_client.get_or_create_collection("pdf_collection")
            
            embeddings = get_embeddings(chunks, embedding_model)
            collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
            
            processed_pdf = ProcessedPDF.objects.create(
                file_name=pdf_file.name,
                processed=True
            )
            
            return Response(ProcessedPDFSerializer(processed_pdf).data, status=201)
        return Response(serializer.errors, status=400)

class QuestionAnswerView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "No question provided"}, status=400)

        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        chroma_client = chromadb.Client()
        collection = chroma_client.get_collection("pdf_collection")
        llm = Ollama(model="mistral")

        relevant_chunks = search_similar_chunks(question, embedding_model, collection)
        context = " ".join(relevant_chunks)
        
        prompt = f"""Based on the following context from a textbook chapter, provide a detailed and comprehensive answer to the question. Your answer should be suitable for a school assignment, demonstrating thorough understanding and covering multiple aspects of the topic.

        Context: {context}

        Question: {question}

        Detailed Answer:"""
        
        response = llm.complete(prompt)
        
        return Response({"answer": response})

class SummarizerView(APIView):
    def post(self, request):
        keywords = request.data.get('keywords')
        llm = Ollama(model="mistral")

        if keywords:
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            chroma_client = chromadb.Client()
            collection = chroma_client.get_collection("pdf_collection")
            summary = summarize_section(collection.get()['documents'], keywords, embedding_model, collection, llm)
        else:
            text = " ".join(collection.get()['documents'])
            summary = summarize_document(text, llm)

        return Response({"summary": summary})

class QuestionGeneratorView(APIView):
    def post(self, request):
        num_questions = request.data.get('num_questions', 5)
        llm = Ollama(model="mistral")
        text = " ".join(chromadb.Client().get_collection("pdf_collection").get()['documents'])
        qa_pairs = generate_qa_pairs(text, num_questions, llm)
        return Response({"qa_pairs": qa_pairs})

class QuestionPaperGeneratorView(APIView):
    def post(self, request):
        num_questions = request.data.get('num_questions', 20)
        previous_paper = request.data.get('previous_paper')
        llm = Ollama(model="mistral")
        text = " ".join(chromadb.Client().get_collection("pdf_collection").get()['documents'])
        question_paper = generate_question_paper(text, llm, num_questions, previous_paper)
        return Response({"question_paper": question_paper})

class StudyPlanGeneratorView(APIView):
    def post(self, request):
        duration_days = request.data.get('duration_days', 7)
        llm = Ollama(model="mistral")
        text = " ".join(chromadb.Client().get_collection("pdf_collection").get()['documents'])
        study_plan = generate_study_plan(text, llm, duration_days)
        return Response({"study_plan": study_plan})