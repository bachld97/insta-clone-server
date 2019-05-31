from django.urls import reverse
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from enum import IntEnum
from django.contrib.auth.models import User

"""
    For later reference of dynamic fields:
    https://django.cowhite.com/blog/dynamic-fields-in-django-rest-framwork-serializers/
"""

class PostInteractionType(IntEnum):
    LIKE = 0
    SHARE = 1

    @classmethod
    def all(self):
        return [
            PostInteractionType.LIKE,
            PostInteractionType.SHARE,
        ]


class Post(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def comments(self):
        comments = Comment.objects.filter(post__pk=self.pk)
        return [c.serialized() for c in comments]

    @property
    def age_in_seconds(self):
        return (timezone.now() - self.created_at).seconds

    @property
    def like_count(self):
        return PostInteraction.objects.filter(
            post__pk=self.id, interaction=PostInteractionType.LIKE
        ).count()

    @property
    def creator_info(self):
        return {
            'id': self.creator.id,
            'username': self.creator.username,
        }


class PostSerializer(serializers.ModelSerializer):
    urls = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    def create(self, validated_data):
        creator = self.context['request'].user
        post = Post(
            caption=validated_data['caption'],
            creator=creator
        )
        post.save()
        return post

    def get_liked_by_user(self, instance):
        uid = instance.creator.id
        return PostInteraction.liked_by_user(user_id=uid)

    def get_urls(self, instance):
        request = self.context.get('request')
        like_url = request.build_absolute_uri(reverse('post-like', kwargs={ 'pk':instance.pk }))
        comment_url = request.build_absolute_uri(reverse('post-comment', kwargs={ 'pk':instance.pk }))
        return {
            'like': like_url,
            'comment': comment_url
        }

    class Meta:
        model = Post
        fields = (
            'id', 'creator_info', 'caption', 'age_in_seconds',
            'like_count', 'urls', 'comments', 'liked_by_user'
        )


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
            'username': self.creator.username,
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
    def liked_by_user(self, user_id):
        likes = PostInteraction.objects.filter(
            user__pk=user_id,
            interaction=PostInteractionType.LIKE
        )
        return len(likes) > 0

    @classmethod
    def create_like(self, post_id, user):
        post_object = Post.objects.get(pk=post_id)
        try:
            like_object = PostInteraction.objects.create(
                post=post_object,
                user=user,
                interaction = PostInteractionType.LIKE
            )
        except:
            return None
        return like_object

    class Meta:
        unique_together = (('interaction', 'user'))

