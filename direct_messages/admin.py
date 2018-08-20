from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sender', 'content',)

admin.site.register(Message, MessageAdmin)
