from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

from .models import Message, ChatRoom
from .signals import message_read, message_sent

from users.models import User

class MessagingService(object):
    """
    A object to manage all messages and conversations.
    """

    # Message creation

    def send_message(self, sender, recipient, message):
        """
        Send a new message
        :param sender: user
        :param recipient: user
        :param message: String
        :return: Messages and status code
        """
        if sender == recipient:
            raise ValidationError("You can't send message to yourself.")

        message = Message(sender=sender, recipient=recipient, content=str(message))
        message.save()

        message_sent.send(sender=message, form_user=message.sender, to=message.recipient)

        # The second value acts as a status value
        return message, 200

    # Message reading

    def get_unread_messages(self, user):
        """
        List of unread messages for a specific user
        :param user: user
        :return: messages
        """
        return Message.objects.all().filter(recipient=user, read_at=None)

    def read_message(self, message_id):
        """
        Read specific message
        :param message_id: Integer
        :return: Message Text
        """
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.content
        except Message.DoesNotExist:
            return ""

    # Helper methods
    def mark_as_read(self, message):
        """
        Marks a message as read, if it hasn't been read before
        :param message: Message
        """
        if message.read_at is None:
            message.read_at = timezone.now()
            message_read.send(sender=message, from_user=message.sender, to=message.recipient)
            message.save()

    def read_meesage_formatted(self, message_id):
        """
        Read a message in the format <User>: <Message>
        :param message_id: Id
        :return: Formatted Message Text
        """
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.sender.username + ": " + message.content
        except Message.DoesNotExist:
            return ""

    # Conversation management

    def get_active_conversations(self, sender, recipient):

        active_conversations = Message.objects.filter(
            (Q(sender=sender) & Q(recipient=recipient))
            | (Q(sender=recipient) & Q(recipient=sender))
        ).order_by('sent_at')

        # print('active conversions', active_conversations)
        return active_conversations

    def get_conversations(self, user):
        """
        Lists all conversation-partners for a specific user
        :param user: User
        :return: Conversation list
        """
        chatrooms = ChatRoom.objects.filter((Q(sender=user) | Q(recipient=user)))

        chatroom_mapper = []
        for chatroom in chatrooms:
            chatroom_dict = {}
            chatroom_dict['pk'] = chatroom.pk

            if user == chatroom.sender:
                recipient = chatroom.recipient
            else:
                recipient = chatroom.sender
            chatroom_dict['recipient'] = recipient
            chatroom_mapper.append(chatroom_dict)

        return chatroom_mapper

        # all_conversations = Message.objects.all().filter(Q(sender=user) | Q(recipient=user))\
        #     .order_by('recipient', 'sent_at')\
        #     .values('pk', 'content', 'sender', 'recipient', 'sent_at').distinct()
        #
        # contacts = {}
        # for conversation in all_conversations:
        #     recp = conversation['recipient']
        #     sndr = conversation['sender']
        #
        #     print('rec and send', recp, sndr)
        #     if conversation['recipient'] != user.pk:
        #         print('entered...', recp)
        #         print('contacts', contacts)
        #         if conversation['recipient'] not in contacts:
        #             print('entered second', recp)
        #             recipient = User.objects.get(pk=conversation['recipient'])
        #             chatroom = ChatRoom.objects.filter(
        #                 (Q(sender__pk=sndr) & Q(recipient__pk=recp))
        #                 | (Q(sender=recp) & Q(recipient=sndr))
        #             ).first()
        #             conversation['recipient'] = recipient
        #             conversation['chat_id'] = chatroom.id
        #             contacts[recp] = conversation
        # return list(contacts.values())

    # def get_conversation(self, user1, user2, limit=None, reversed=False, mark_read=False):
    #     """
    #     List of messages between two users
    #     :param user1: User
    #     :param user2: User
    #     :param limit: int
    #     :param reversed: Boolean - Makes the newest message be at index 0
    #     :param mark_read:
    #     :return: messages
    #     """
    #     users = [user1, user2]
    #
    #     # Newest message first if it's reversed (index 0)
    #     if reversed:
    #         order = '-pk' # DESC
    #     else:
    #         order = 'pk' # ASC
    #
    #     conversation = Message.objects.all().filter(sender__in=users, recipient__in=users).order_by(order)
    #
    #     if limit:
    #         # Limit number of messages to the x newest
    #         conversation = conversation[:limit]
    #
    #     if mark_read:
    #         for message in conversation:
    #             # Just to be sure, everything is read
    #             self.mark_as_read(message)
    #
    #     return conversation



