from rest_framework import serializers
from django.urls import reverse
from .models.posts import Post, PostContent
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
    content = serializers.SerializerMethodField()

    def create(self, validated_data):
        creator = self.context['request'].user
        images = self.context['request'].FILES.getlist('images[]')
        post = Post.create_new(
            caption=validated_data['caption'],
            images=images,
            creator=creator
        )
        return post

    def get_liked_by_user(self, instance):
        creator = instance.creator
        if creator is None:
            return False
        uid = creator.id
        return PostInteraction.liked_by_user(post=instance, user_id=uid)

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
        comments = Comment.objects.filter(post__pk=instance.pk).select_related('post')
        return [c.serialized() for c in comments]

    def get_content(self, instance):
        images = PostContent.objects.filter(post__pk=instance.pk).select_related('post')
        request = self.context.get('request')
        return [request.build_absolute_uri(i.image.url) for i in images]

    class Meta:
        model = Post
        fields = (
            'id', 'creator_info', 'caption', 'age_in_seconds',
            'like_count', 'urls', 'comments', 'liked_by_user',
            'content'
        )

