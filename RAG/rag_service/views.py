# views.py
import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .processing import process_document


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import tempfile
import os


class DocumentProcessingView(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        try:
            result = process_document(temp_path, request)  # передаем путь к файлу
            return Response({"status": "ready", "result": result})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)  # Удаляем временный файл
