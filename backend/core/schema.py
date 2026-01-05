import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterBackend
from graphql import GraphQLError

from django.contrib.auth import get_user_model
from groups.models import Group, Thread, Membership
from chat.models import Message

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'is_staff')

class GroupType(DjangoObjectType):
    member_count = graphene.Int()
    thread_count = graphene.Int()
    user_role = graphene.String()

    class Meta:
        model = Group
        fields = ('id', 'name', 'username', 'is_private', 'created_by', 'created_at')

    def resolve_member_count(self, info):
        return self.mebers.count()
    
    def resolve_thread_count(self, info):
        return self.thread.count()
    
    def resolve_user_role(self, info):
        user = info.context.user
        if user.is_authenticated:
            membership = Membership.objects.filter(user=user, group=self).first()
            return membership.role if membership else None 
        return None
    
class ThreadType(DjangoObjectType):
    message_count = graphene.Int()
    
    class Meta:
        model = Thread
        fields = ('id', 'group', 'subject', 'created_by', 'created_at', 'updated_at')

    def resolve_message_count(self, info):
        return self.message.count()
    
class MessageType(DjangoObjectType):
    replies = graphene.List(lambda: MessageType)

    class Meta:
        model = Message
        fields = ('id', 'thread', 'text', 'author', 'parent_message', 'created_at')
    
    def resolve_replies(self, info):
        return Message.objects.filter(parent_message=self)

class MembershipType(DjangoObjectType):
    class Meta:
        model = Membership
        fields = ('id', 'user', 'group', 'role', 'joined_at')

# GRAPH QL QUERIES

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    group = graphene.Field(GroupType, id=graphene.Int())
    thread = graphene.Field(ThreadType, id=graphene.Int())
    message = graphene.Field(MessageType, id=graphene.Int())

    all_groups = graphene.List(
        GroupType,
        is_private=graphene.Boolean(),
        search=graphene.String()
    )

    my_groups = graphene.List(GroupType)

    threads_by_group = graphene.List(ThreadType, group_id=graphene.Int(required=True))
    messages_by_thread = graphene.List(MessageType, thread_id=graphene.Int(required=True))
    