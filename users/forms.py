from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, ReadOnlyPasswordHashField
)
from django.db import transaction

from .models import User

# class SignUpForm(UserCreationForm):
#     pass

class UserCreationForm(forms.ModelForm):
    pass

class UserChangeForm(forms.ModelForm):
    pass

class FreelancerSignUpForm(UserCreationForm)
    pass

class OwnerSignUpForm(UserCreationForm):
    pass

