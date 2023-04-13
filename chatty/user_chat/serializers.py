from rest_framework import serializers
from user_chat.models import UserThread, UserMessage


class UserThreadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for UserThread model.
    It has 'user' field that is write-only, required
    and takes an integer value representing the id of the other user in the thread.
    The validate() method checks whether the thread creator
     and the other user are the same and raises a validation error if they are the same.
    The create() method creates a new UserThread object
    if the thread between the creator and the other user doesn't already exist.
    """
    user = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = UserThread
        fields = [
            'id',
            'participants',
            'updated',
            'created',
            'user'
        ]
        read_only_fields = ['id', 'created', 'updated', 'participants']

    def validate(self, attrs):
        user = attrs.pop('user')
        request_user = self.context['request'].user.pk
        if request_user == user:
            raise serializers.ValidationError('User cannot start a thread with themselves.')

        attrs['user'] = user
        attrs['participants'] = [user, request_user]
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        participants = validated_data.get('participants')
        request_user = self.context['request'].user.pk

        thread = UserThread.get_user_thread(request_user, user)
        if thread:
            return thread

        thread = UserThread.objects.create()
        thread.participants.set(participants)
        thread.save()
        return thread


class UserMessagesSerializer(serializers.ModelSerializer):
    """
    This serializer is used for UserMessage model.
    The create() method creates
    a new UserMessage object with the authenticated user as the sender,
    the UserThread object with the given 'user_id', and the given text.
    """

    class Meta:
        model = UserMessage
        fields = [
            'id',
            'sender',
            'text',
            'created',
            'is_read',
        ]
        read_only_fields = ['id', 'sender', 'created']

    def create(self, validated_data):
        text = validated_data['text']
        user = self.context['request'].user
        thread = UserThread.get_user_thread(user.id, self.context['user_id'])

        message = UserMessage.objects.create(
            sender=user,
            thread=thread,
            text=text
        )
        message.save()
        return message
