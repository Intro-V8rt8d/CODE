from django import forms
from .models import Assignment, ObjectiveQuestion, Option

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title","question_text","question_file","deadline","submit_here"]

class ObjectiveForm(forms.Form):
    question = forms.CharField()
    option_a = forms.CharField()
    option_b = forms.CharField()
    option_c = forms.CharField(required=False)
    option_d = forms.CharField(required=False)
    correct = forms.ChoiceField(choices=[("A","A"),("B","B"),("C","C"),("D","D")])
