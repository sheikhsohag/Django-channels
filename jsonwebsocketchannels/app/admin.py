from django.contrib import admin
from . models import Chat, Group
# Register your models here.


@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id','group', 'timestamp', 'content']

@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']