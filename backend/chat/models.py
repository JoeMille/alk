from django.conf import settings
from django.db import models


class Message(models.Model):
    thread = models.ForeignKey(
        "groups.Thread", on_delete=models.CASCADE, related_name="messages"
    )

    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )

    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"

    class Meta:
        ordering = ["-created_at"]
