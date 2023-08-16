from django.db import models

class VoiceResult(models.Model):
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)