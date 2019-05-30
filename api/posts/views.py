from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, PostSerializer, PostInteraction, Comment

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        content = request.data['content']
        comment_object = Comment.create_for(
            post_id=pk, user=request.user, content=content
        )
        if comment_object is None:
            return Response(
                { 'error' : 'Cannot comment on this post' },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            comment_object.serialized(),
            status = status.HTTP_201_CREATED
        )


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        like_object = PostInteraction.create_like(post_id=pk, user=request.user)
        if like_object is None:
            return Response(
                { 'error' : 'Cannot create like for this post' },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            { 'success': 'Like created' },
            status=status.HTTP_201_CREATED
        )