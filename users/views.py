from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic import (
    TemplateView, UpdateView,
    CreateView, ListView,
)

from .models import User
from .forms import FreelancerSignUpForm, OwnerSignUpForm

class SignUpView(TemplateView):
    template_name = 'users/signup.html'

class UserDetailView(TemplateView):
    model = User
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):
        """
        Prepares user context value based on username request from url.
        """
        context = super(UserDetailView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = User.objects.get(username=username)
        return context

class UpdateProfileView(UpdateView):
    """
    Update the profile.
    """
    model = User
    fields = ['profile_photo', 'first_name', 'last_name', 'profile', 'skills'] # Keep listing whatever fields
    template_name = 'users/user_profile_update.html'

    def form_valid(self, form):
        """
        Checks valid form and add/save many to many tags field in user object.
        """
        user = form.save(commit=False)

        user.save()
        form.save_m2m()
        messages.success(self.request, 'Your profile is updated successfully.')
        return redirect('users:user_profile', self.object.username)

    def get_success_url(self):
        """
        Prepares success url for successful form submission.
        """
        return reverse('users:user_profile', kwargs={'username': self.object.username})


class ListFreelancersView(ListView):
    """
    Show all Freelancers.
    """
    model = User
    context_object_name = 'freelancers'
    template_name = 'users/freelancer_list.html'

    def get_queryset(self):
        """
        Prepare all freelancers based on is_freelancer col in user model.
        """
        return User.objects.filter(is_freelancer=True)

class FreelancerSignUpView(CreateView):
    """
    Register a freelancer.
    """
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        """
        Updates context value 'user_type' in curernt context.
        """
        kwargs['user_type'] = 'freelancer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
