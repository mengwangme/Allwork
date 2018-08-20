from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Message(models.Model):
    """
    A private direct message.
    """
    content = models.TextField('Content')
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_dm', verbose_name='Sender'
    )
    recipient = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_dm', verbose_name='Recipient'
    )
    sent_at = models.DateTimeField('sent at', auto_now_add=True)
    read_at = models.DateTimeField('read at', null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    @property
    def unread(self):
        """
        Returns whether the message was read or not.
        """
        if self.read_at is not None:
            return True

    def __str__(self):
        return self.content

    def save(self, **kwargs):
        """
        Check message sender and recipient and raise error if the are saved.
        Save message when the condition passes.
        """
        if self.sender == self.recipient:
            raise ValidationError("You cant't send messages to yourself!")

        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

class ChatRoom(models.Model):
    """
    A private char room

    Attributes:
        created_at (datetime): datetime value when chatroom is created.
        recipient (user): user whom the chatroom sends first message.
        sender (user): user who created the chatroom
    """
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chatroom_sender', verbose_name='Sender'
    )
    recipient = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chatroom_recipient'
    )
    created_at = models.DateTimeField('sent at', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('sender', 'recipient')