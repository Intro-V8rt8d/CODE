from django import forms
from .models import Video, Document, Category

class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search")

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title","youtube_id","category"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title","file","category"]
