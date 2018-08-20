from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import (
    UserDetailView, UpdateProfileView,
    FreelancerSignUpView, OwnerSignUpView,
    ListFreelancersView, home,
    SignUpView, UserJobProfile
)

app_name = 'users'

urlpatterns = [
    # path('', home, name='home'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(([
        path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('signup/freelancer/', FreelancerSignUpView.as_view(), name='freelancer_signup'),
        path('signup/project-owner/', OwnerSignUpView.as_view(), name='owner_signup'),
    ]))),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # path('accounts/signup/freelancer/', FreelancerSignUpView.as_view(), name='freelancer_signup'),
    # path('accounts/signup/project-owner/', OwnerSignUpView.as_view(), name='owner_signup'),
    path('freelancers/', include(([
        path('', ListFreelancersView.as_view(), name='list_freelancer'),
        path('<str:username>', UserDetailView.as_view(), name='freelancer_detail'),
    ]))),
    # path('freelancers/', ListFreelancersView.as_view(), name='list_freelancer'),
    # path('freelancers/<str:username>', UserDetailView.as_view(), name='freelancer_detail'),
    path('user/', include(([
        path('<str:pk>/edit', UpdateProfileView.as_view(), name="update_profile"),
        path('<str:username>/', UserDetailView.as_view(), name='user_profile'),
        path('<str:username>/jobs/', UserJobProfile.as_view(), name='job_profile'),
    ]))),
    # path('user/<str:pk>/edit', UpdateProfileView.as_view(), name="update_profile"),
    # path('user/<str:username>/', UserDetailView.as_view(), name='user_profile'),
    # path('user/<str:username>/jobs', UserJobProfile.as_view(), name='job_profile'),

]
