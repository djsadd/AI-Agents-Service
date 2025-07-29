# urls.py
from django.urls import path
from .views import DocumentUploadView


# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import DocumentViewSet, ChunkViewSet, EmbeddingViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'chunks', ChunkViewSet)
router.register(r'embeddings', EmbeddingViewSet)


urlpatterns = [
    path('upload/<int:project_id>/', DocumentUploadView.as_view(), name='document_upload'),
]
urlpatterns += router.urls  # ← добавляем роутер сюда без обёртки в path('api/')