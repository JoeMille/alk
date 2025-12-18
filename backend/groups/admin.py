from django.contrib import admin
from .models import Group, Membership, Thread

admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Thread)
