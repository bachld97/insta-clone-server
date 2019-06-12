from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .posts import Post

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def age_in_seconds(self):
        return (timezone.now() - self.created_at).seconds

    @property
    def creator_info(self):
        return {
            'id': self.creator.id,
            'name': self.creator.username,
        }

    @classmethod
    def create_for(self, post_id, user, content):
        post_object = Post.objects.get(pk=post_id)
        comment_object = Comment.objects.create(
            post=post_object,
            creator=user,
            content = content
        )
        return comment_object

    def serialized(self):
        return {
            'id': self.pk,
            'creator': self.creator_info,
            'content': self.content,
            'age_in_seconds': self.age_in_seconds
        }
