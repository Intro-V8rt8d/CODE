from django.db import models
from django.contrib.auth.models import User
import secrets, string

def gen_room():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))

class LiveSession(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lives")
    room = models.CharField(max_length=8, unique=True, default=gen_room)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self): return f"{self.tutor.username} / {self.room}"

class Participant(models.Model):
    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    kicked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("session","user")
