from django.db import models
from django.contrib.postgres.fields import ArrayField

from azura_be.base.constants import CommunicationMessageType
from azura_be.base.models import BaseModel
from azura_be.business_accounts.models import BusinessAccount
from azura_be.users.models import User


class CommunicationMessage(BaseModel):
    destination_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="communications")
    type = models.CharField(max_length=10, choices=CommunicationMessageType)
    destination = models.CharField(max_length=150)
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    read = models.BooleanField(default=False)
    account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name="communications")
    provider_groups = ArrayField(models.UUIDField(), null=True, blank=True)

    def send(self):
        if self.type == CommunicationMessageType.EMAIL.name:
            return self.send_email()
        elif self.type == CommunicationMessageType.SMS_TEXT:
            return self.send_sms()
        return self.send_in_app()

    def send_email(self):
        pass

    def send_sms_text(self):
        pass

    def send_in_app(self):
        pass


class Thread(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    is_group = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_threads")
    picture = models.FileField(upload_to="threads/", null=True, blank=True)


class ThreadUser(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_threads")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="added_threads_users")


class ThreadMessage(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread_messages")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="thread_messages_send")
    content = models.TextField(blank=True)
    has_attachment = models.BooleanField(default=False)
    read = models.BooleanField(default=False)


class ThreadAttachment(BaseModel):
    thread_message = models.ForeignKey(ThreadMessage, on_delete=models.CASCADE, related_name="thread_message_attachments")
    file = models.FileField(upload_to="thread_attachments/")
    ext = models.CharField(max_length=50)
