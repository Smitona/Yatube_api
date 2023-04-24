from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend


from posts.models import Group, Post, Comment, User, Follow
from api.serializers import (
    PostSerializer, GroupSerializer, CommentSerializer,
    UserSerializer, FollowSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise PermissionDenied('Нельзя редактировать чужой комметарий!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise PermissionDenied('Удалять чужие комментарии нельзя!')
        super(CommentViewSet, self).perform_destroy(serializer)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.select_related('user')
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self, *args, **kwargs):
        return Follow.objects.all().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
