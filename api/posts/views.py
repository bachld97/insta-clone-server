from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostSerializer
from .models.post_comments import Comment
from .models.post_interactions import PostInteraction
from .models.posts import Post

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(
        creator__isnull=False
    ).select_related('creator')
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        content = request.data['content']
        comment_object = Comment.create_for(
            post_id=pk, user=request.user, content=content
        )
        if comment_object is None:
            return Response(
                { 'error' : 'Post does not exists.' },
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
                { 'success': False, 'error': 'Post does not exist or already liked.' },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            { 'success': True },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        like_object = PostInteraction.delete_like(post_id=pk, user_id=request.user.id)
        return Response(
            { 'success': 'True' },
            status=status.HTTP_202_ACCEPTED
        )
