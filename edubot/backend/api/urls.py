from django.urls import path
from .views import (
    PDFProcessView,
    QuestionAnswerView,
    SummarizerView,
    QuestionGeneratorView,
    QuestionPaperGeneratorView,
    StudyPlanGeneratorView
)

urlpatterns = [
    path('process-pdf/', PDFProcessView.as_view(), name='process-pdf'),
    path('question-answer/', QuestionAnswerView.as_view(), name='question-answer'),
    path('summarize/', SummarizerView.as_view(), name='summarize'),
    path('generate-questions/', QuestionGeneratorView.as_view(), name='generate-questions'),
    path('generate-question-paper/', QuestionPaperGeneratorView.as_view(), name='generate-question-paper'),
    path('generate-study-plan/', StudyPlanGeneratorView.as_view(), name='generate-study-plan'),
]
