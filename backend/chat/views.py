from rest_framework import viewsets, permissions
from django.db.models import Q 

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        thread_id = self.request.query_params.get('thread')
        queryset = Message.objects.all()

        if thread_id:
            queryset = queryset.filter(thread_id=thread_id)
        
        return queryset.filter(
            thread__group__members=user
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)