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

    @action(detail=True, methods=['post', 'get'])
    def comment(self, request, pk=None):
        if (request.method == 'POST'):
            return self.__new_comment__(request, pk)
        else:
            return self.__list_comments__(request, pk)
    
    def __new_comment__(self, request, pk=None):
        content = request.data.get('content', request.query_params.get('content', None))
        if content is None:
            return Response(
                { 'error' : 'Content must be passed in query parameters or in body.' },
                status=status.HTTP_400_BAD_REQUEST
            )

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


    def __list_comments__(self, request, pk=None):
        last_comment_id = request.data.get(
            'lastCommentId', request.query_params.get('lastCommentId', 0)
        )
        comments = Comment.objects.filter(
            pk__gt=last_comment_id,
            post__pk=pk
        ).select_related('post', 'creator')
        data = [comment.serialized() for comment in comments]
        return Response(
            data, status=status.HTTP_200_OK
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
