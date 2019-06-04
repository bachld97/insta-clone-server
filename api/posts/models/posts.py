from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def age_in_seconds(self):
        return (timezone.now() - self.created_at).seconds

    @property
    def creator_info(self):
        return {
            'id': self.creator.id,
            'username': self.creator.username,
        }

