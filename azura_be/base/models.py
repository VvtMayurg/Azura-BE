import uuid

from django.contrib.auth import get_user_model
from django.db import models

from azura_be.base.context import current_context

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = getattr(current_context, "user", None)
        if isinstance(user, User):
            if not self.pk:
                self.created_by = self.created_by if self.created_by else user.pk
                self.updated_by = self.updated_by if self.updated_by else user.pk
            else:
                self.updated_by = self.updated_by if self.updated_by else user.pk
        super().save(*args, **kwargs)
