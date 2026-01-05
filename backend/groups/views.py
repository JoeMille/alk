from django.db import models 
from rest_framework import viewsets, permissions, status 
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Group, Membership, Thread
from .serializers import (
    GroupListSerializer,
    GroupDetailSerializer,
    GroupCreateSerializer,
    MembershipSerializer,
    ThreadSerializer,
)

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        if self.action == 'retrieve':
            return GroupDetailSerializer
        if self.action == 'create':
            return GroupCreateSerializer
        if self.action in ('join', 'leave'):
            return MembershipSerializer
        return GroupDetailSerializer 

    def get_queryset(self):
        # ========== FIXED: Return Groups, not Threads ==========
        user = self.request.user
        return Group.objects.filter(
            models.Q(is_private=False) | models.Q(members=user)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()

        if group.is_private:
            return Response(
                {"error": "Cannot join priv group"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        membership, created = Membership.objects.get_or_create(
            user=request.user,
            group=group,
            defaults={'role': 'member'}
        )

        if not created: 
            return Response(
                {"error": "already member"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            MembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()

        try:
            membership = Membership.objects.get(user=request.user, group=group)

            if membership.role == 'admin':
                admin_count = Membership.objects.filter(
                    group=group,
                    role='admin'
                ).count()

                if admin_count == 1:
                    return Response(
                        {"error": "Cannot leave. Only admin account."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Membership.DoesNotExist:
            return Response(
                {"error": "Not a group member"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ThreadViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThreadSerializer  

    def get_queryset(self):
        user = self.request.user
        group_id = self.request.query_params.get('group')
        queryset = Thread.objects.all()

        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        return queryset.filter(
            group__members=user
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)