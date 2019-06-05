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
        if self.creator is None:
            return None

        return {
            'id': self.creator.id,
            'username': self.creator.username,
        }


    @classmethod
    def create_new(self, caption, images, creator):
        post = Post(
            caption=caption,
            creator=creator
        )
        post.save()
        for image in images:
            self.__handle_upload__(image=image, post=post)
        return post

    @classmethod
    def __handle_upload__(self, image, post):
        try:
            PostContent.objects.create(
                post=post,
                image=image
            )
        except:
            pass


class PostContent(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='images/')
