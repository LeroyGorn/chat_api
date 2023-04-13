from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_chat.models import UserThread, UserMessage
from user_chat.serializers import UserThreadSerializer, UserMessagesSerializer


class UserThreadListCreateView(generics.ListCreateAPIView):
    """
     This view handles the creation and listing of threads related to a user.
     It requires the user to be authenticated and provides a pagination option.
     The get_queryset() method is used to get all threads related to the authenticated user.
    """
    permission_classes = (
        IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
    serializer_class = UserThreadSerializer

    def get_queryset(self):
        user = self.request.user
        return user.threads.all()


class UserThreadListView(generics.ListCreateAPIView):
    """
    This view handles the listing of messages related to a specific thread between two users.
     It requires the user to be authenticated and provides a pagination option.
     The get() method is used to retrieve the thread between the authenticated user and another user.
     It then retrieves all messages associated with that thread and returns them in the response.
    """
    permission_classes = (
        IsAuthenticated,
    )
    pagination_class = LimitOffsetPagination
    serializer_class = UserMessagesSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.kwargs.get('user_id')
        return context

    def get(self, *args, **kwargs):
        request_user_id = self.request.user.id
        user_id = self.kwargs.pop('user_id')

        thread = UserThread.get_user_thread(request_user_id, user_id)
        if request_user_id == user_id or not thread:
            raise NotFound()

        messages = UserMessage.objects.filter(thread=thread)
        return Response({
            'messages': UserMessagesSerializer(messages, many=True).data,
            'thread': UserThreadSerializer(thread).data,
        }, status=status.HTTP_200_OK)


class UserMessagesUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles the update and deletion of specific messages.
     It requires the user to be authenticated and provides a serializer to serialize the message data.
     The get_object() method is used to retrieve the message by its ID,
     and the delete() method is used to delete the message.
    """
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UserMessagesSerializer

    def get_object(self):
        return get_object_or_404(UserMessage, id=self.kwargs.pop('message_id'))

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserThreadDeleteView(generics.DestroyAPIView):
    """
    This view handles the deletion of a thread between two users.
    It requires the user to be authenticated, and the thread must be related to the authenticated user.
    The get_object() method is used to retrieve the thread by its ID,
    and the delete() method is used to delete the thread.
    """
    permission_classes = (
        IsAuthenticated,
    )

    def get_object(self):
        return get_object_or_404(UserThread, id=self.kwargs.pop('thread_id'))

    def delete(self, request, *args, **kwargs):
        thread = self.get_object()
        if request.user not in thread.participants.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMessagesView(generics.ListAPIView):
    """
    This view handles the listing of unread messages related to a user.
    It requires the user to be authenticated and provides a pagination option.
     The get_queryset() method is used to retrieve all unread messages
     associated with any thread that the user is a participant in.
    """
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UserMessagesSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        threads = UserThread.objects.filter(participants__id=user.id)
        return UserMessage.objects.filter(
            Q(is_read=False) & ~Q(sender=user) & Q(thread__in=threads)
        )
