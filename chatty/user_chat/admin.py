from django.contrib import admin

from user_chat.models import UserThread, UserMessage


@admin.register(UserThread)
class UserThreadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'updated')
    filter_horizontal = ('participants',)


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sender', 'thread', 'created', 'is_read')
    list_filter = ('is_read', 'created')
    search_fields = ('text', 'sender__email', 'thread__id')
