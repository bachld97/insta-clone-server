from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from enum import IntEnum
from .posts import Post

class PostInteractionType(IntEnum):
    LIKE = 0
    SHARE = 1

    @classmethod
    def all(self):
        return [
            PostInteractionType.LIKE,
            PostInteractionType.SHARE,
        ]


class PostInteraction(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    interaction = models.IntegerField(
        choices=[
            (interaction.name, interaction.value) for interaction in PostInteractionType.all()
        ]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    @classmethod
    def liked_by_user(self, post, user_id):
        likes = PostInteraction.objects.filter(
            post__pk=post.pk,
            user__pk=user_id,
            interaction=PostInteractionType.LIKE
        ).select_related('user', 'post')
        return likes.exists()


    @classmethod
    def delete_like(self, post_id, user_id):
        likes = PostInteraction.objects.filter(
            post__pk=post_id,
            user__pk=user_id,
            interaction=PostInteractionType.LIKE
        ).select_related('post', 'user')
        for like in likes:
            like.delete()


    @classmethod
    def create_like(self, post_id, user):
        try:
            post_object = Post.objects.get(pk=post_id)
            like_object = PostInteraction.objects.create(
                post=post_object,
                user=user,
                interaction = PostInteractionType.LIKE
            )
        except Exception as error:
            print(error)
            return None
        return like_object


    @classmethod
    def like_count(self, post_id):
        count = PostInteraction.objects.filter(
            post__pk=post_id, interaction=PostInteractionType.LIKE
        ).count()
        return count

    class Meta:
        unique_together = (('post', 'interaction', 'user'))


