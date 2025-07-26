from django.contrib import admin
from .models import Document, Chunk, Embedding
# Register your models here.


admin.site.register(Document)
admin.site.register(Chunk)
admin.site.register(Embedding)