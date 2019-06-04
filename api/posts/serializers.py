from rest_framework import serializers
from django.urls import reverse
from .models.posts import Post
from .models.post_interactions import PostInteraction
from .models.post_comments import Comment

"""
    For later reference of dynamic fields:
    https://django.cowhite.com/blog/dynamic-fields-in-django-rest-framwork-serializers/
"""

class PostSerializer(serializers.ModelSerializer):
    urls = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

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

    def get_like_count(self, instance):
        return PostInteraction.like_count(post_id=instance.pk)

    def get_comments(self, instance):
        comments = Comment.objects.filter(post__pk=instance.pk)
        return [c.serialized() for c in comments]

    class Meta:
        model = Post
        fields = (
            'id', 'creator_info', 'caption', 'age_in_seconds',
            'like_count', 'urls', 'comments', 'liked_by_user'
        )


