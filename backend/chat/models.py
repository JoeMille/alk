from django.db import models

class Message(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text[:50]}"
    
    class Meta:
        ordering = ['-created_at']