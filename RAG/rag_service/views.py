# views.py
import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .processing import process_document


class DocumentProcessingView(APIView):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем файл во временный путь
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            for chunk in file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        try:
            result = process_document(tmp_file_path)
            os.remove(tmp_file_path)  # Удалить временный файл
            return Response({"status": "ready", "result": result})
        except Exception as e:
            os.remove(tmp_file_path)
            return Response({"status": "error", "message": str(e)}, status=500)
