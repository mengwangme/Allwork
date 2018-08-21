from django.urls import path, include

from .views import MessageView, MessageDetailView

app_name = 'direct_messages'

urlpatterns = [
    path('messages/', include(([
        path('', MessageView.as_view(), name='list_message'),
        path('<int:pk>/', MessageDetailView.as_view(), name='user_message'),
    ])))
]