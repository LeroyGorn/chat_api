from django.urls import path

from user_chat.views import (
    UserThreadListCreateView,
    UserThreadListView,
    UserThreadDeleteView,
    UserMessagesView,
    UserMessagesUpdateDeleteView
)

urlpatterns = [
    path('', UserThreadListCreateView.as_view()),
    path('<int:user_id>/', UserThreadListView.as_view()),
    path('message/<int:message_id>/', UserMessagesUpdateDeleteView.as_view()),
    path('thread_delete/<int:thread_id>/', UserThreadDeleteView.as_view()),
    path('unread/', UserMessagesView.as_view()),
]
