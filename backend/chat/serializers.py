from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )

    # Expose related obj names 
    thread_subject = serializers.CharField(
        source='thread.subject',
        read_only=True
    )

    class Meta:
        model = Message
        fields = (
            'id',
            'thread',
            'text',
            'author',
            'author_username',
            'thread_subject',
            'parent_message',
            'created_at',
        ) 

        read_only_fields = ('id', 'author', 'author_username', 'thread_subject', 'created_at')
