from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, PostSerializer, PostInteraction

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        return Response(
            { 'error' : 'Cannot create like for this post' },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        username = request.user

        like_object = PostInteraction.create_like(post_id=pk, user=user)
        if like_object is None:
            return Response(
                { 'error' : 'Cannot create like for this post' },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'success': 'Like created'},
            status=status.HTTP_201_CREATED
        )
