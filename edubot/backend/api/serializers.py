from rest_framework import serializers
from .models import ProcessedPDF

class PDFUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class ProcessedPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedPDF
        fields = ['id', 'file_name', 'uploaded_at', 'processed']