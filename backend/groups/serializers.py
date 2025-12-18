from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Group, Membership, Thread

User = get_user_model()


class MembershipSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Membership
        fields = (
            "id",
            "user",
            "group",
            "group_name",
            "role",
            "joined_at",
        )
        read_only_fields = ("id", "joined_at")


class GroupListSerializer(serializers.ModelSerializer):

    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    member_count = serializers.SerializerMethodField()
    thread_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "is_private",
            "created_by_username",
            "created_at",
            "member_count",
            "thread_count",
        )
        read_only_fields = ("id", "created_at")

    def get_member_count(self, obj):
        return obj.members.count()

    def get_thread_count(self, obj):
        return obj.threads.count()


class GroupDetailSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)
    memberships = MembershipSerializer(
        many=True, read_only=True, source="membership_set"
    )
    member_count = serializers.SerializerMethodField()
    thread_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "is_private",
            "created_by",
            "created_at",
            "memberships",
            "member_count",
            "thread_count",
            "is_member",
            "user_role",
        )
        read_only_fields = ("id", "created_at", "created_by")

    def get_member_count(self, obj):
        return obj.members.count()

    def get_thread_count(self, obj):
        return obj.threads.count()

    def get_is_member(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.members.filter(id=request.user.id).exists()
        return False

    def get_user_role(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            try:
                membership = Membership.objects.get(user=request.user, group=obj)
                return membership.role
            except Membership.DoesNotExist:
                return None
        return None


class GroupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            "name",
            "description",
            "is_private",
        )

    def create(self, validated_data):

        request = self.context.get("request")

        group = Group.objects.create(created_by=request.user, **validated_data)

        Membership.objects.create(user=request.user, group=group, role="admin")

        return group

class ThreadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'group',
            'subject',
            'created_by',
            'created_by_username',
            'created_at',
            'updated_at',
            'message_count',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    def get_message_count(self, obj):
        return obj.messages.count()
    
    def validate_group(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if not value.members.filter(id=request.user.id).exists():
                raise serializers.ValidationError(
                    "You must be a member of this group to create threads"
                )
        return value