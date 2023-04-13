from django.db import models
from django.db.models.signals import m2m_changed


class UserThread(models.Model):
    participants = models.ManyToManyField(
        to='auth_user.CustomUser',
        related_name='threads'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'Thread {self.pk}'

    @classmethod
    def get_user_thread(cls, request_user_id, user_id):
        """
        Requiring ids of two users.
        Returning a thread in which two users with specified ids taking part.
        """
        return UserThread.objects.filter(
            participants__id=request_user_id
        ).filter(
            participants__id=user_id
        ).first()

    class Meta:
        ordering = ['-updated']


def ensure_two_participants(sender, instance, action, **kwargs):
    if action == 'pre_add' and instance.participants.count() + len(kwargs['pk_set']) > 2:
        raise ValueError('Thread can not have more than 2 participants.')


m2m_changed.connect(ensure_two_participants, sender=UserThread.participants.through)


class UserMessage(models.Model):
    sender = models.ForeignKey(
        to='auth_user.CustomUser',
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )

    text = models.TextField()

    thread = models.ForeignKey(
        to='user_chat.UserThread',
        on_delete=models.CASCADE,
        related_name='messages'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'Message {self.pk}'

    class Meta:
        ordering = ['-created']
