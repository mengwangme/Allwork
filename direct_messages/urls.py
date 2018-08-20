from django.urls import path, include

from .views import MessageView, MessageDetailView


urlpatterns = [
    path('messages/', include(([
        path('', MessageView.as_view(), name='list_message'),
        path('<int:pk>', MessageDetailView.as_view(), name='user_message'),
    ], 'direct_messages'), namespace='direct_messages'))
]