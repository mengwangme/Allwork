from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction

from .models import User

class UserCreationForm(forms.ModelForm):
    """
    ????????
    """
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput) # ????


    class Meta:
    	 # ??????
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_password(self):
        # ??????????
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # ?????????
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.
    Includes all the fields on the user, but replaces the
    password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value.
        return self.initial["password"]


class FreelancerSignUpForm(UserCreationForm):

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_freelancer = True
        user.save()
        return user


class OwnerSignUpForm(UserCreationForm):

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_owner = True
        if commit:
            user.save()
        return user

