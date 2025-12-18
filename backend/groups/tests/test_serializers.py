from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from groups.models import Group, Membership
from groups.serializers import (GroupCreateSerializer, GroupDetailSerializer,
                                GroupListSerializer, MembershipSerializer)

User = get_user_model()


class GroupSerializerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@bs.com", password="testpassword123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@bs.com", password="testpassword123"
        )

        self.group = Group.objects.create(
            name="TestGroup", description="Test desc", created_by=self.user1
        )

        Membership.objects.create(user=self.user1, group=self.group, role="admin")

        Membership.objects.create(user=self.user2, group=self.group, role="member")

    def test_group_list_serializer(self):
        serializer = GroupListSerializer(self.group)
        data = serializer.data

        self.assertEqual(data["name"], "TestGroup")  # Fixed: matches setUp()
        self.assertEqual(data["created_by_username"], "user1")
        self.assertEqual(data["member_count"], 2)
        self.assertEqual(data["thread_count"], 0)
        self.assertNotIn("memberships", data)

    def test_group_detail_serializer(self):
        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = self.user1

        serializer = GroupDetailSerializer(self.group, context={"request": request})
        data = serializer.data

        self.assertEqual(data["name"], "TestGroup")  # Fixed: matches setUp()

        self.assertEqual(data["created_by"]["username"], "user1")

        self.assertEqual(len(data["memberships"]), 2)

        self.assertTrue(data["is_member"])
        self.assertEqual(data["user_role"], "admin")

    def test_group_create_serializer(self):
        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = self.user1

        data = {
            "name": "New Group",
            "description": "New description",
            "is_private": False,
        }

        serializer = GroupCreateSerializer(data=data, context={"request": request})

        self.assertTrue(serializer.is_valid())

        group = serializer.save()

        self.assertEqual(group.name, "New Group")
        self.assertEqual(group.created_by, self.user1)

        membership = Membership.objects.get(user=self.user1, group=group)
        self.assertEqual(membership.role, "admin")
