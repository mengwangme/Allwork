from django.forms import ModelForm
from django import forms

from .models import Message


class MessageForm(ModelForm):

    content = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'write_msg', 'name': 'content', 'placeholder': 'Reply...'}
        )
    )

    class Meta:
        model = Message
        fields = ['content']

