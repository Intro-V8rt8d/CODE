from django.db import models
from django.contrib.auth.models import User
import secrets, string

def gen_code(length=8):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class Assignment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True, default=gen_code)
    title = models.CharField(max_length=200)
    question_text = models.TextField(blank=True)
    question_file = models.FileField(upload_to="assignments/", blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    submit_here = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.title} [{self.code}]"

class ObjectiveQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=300)

class Option(models.Model):
    question = models.ForeignKey(ObjectiveQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_file = models.FileField(upload_to="submissions/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    class Meta:
        unique_together = ("assignment","student")
