from django.contrib import admin
from .models import Category, Video, Document, ResourceSaved
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Document)
admin.site.register(ResourceSaved)
