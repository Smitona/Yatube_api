import base64

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.core.files.base import ContentFile

from posts.models import Post, Group, Comment, User, Follow

from rest_framework import mixins


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin):
    pass


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


def unique_fields(Model, field_1, field_2, msg):
    return [
        UniqueTogetherValidator(
            queryset=Model.objects.all(),
            fields=(field_1, field_2),
            message=msg
        )
    ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')

        msg = "Вы уже создали пост с таким содержанием!"

        # validators = unique_fields(Post, 'text', 'author', msg)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')

        msg = "Вы уже оставили такой комментарий, не спамьте!"

        validators = unique_fields(Comment, 'text', 'author', msg)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        required=False,
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

        msg = "Вы уже подписаны на этого автора!"

        validators = unique_fields(Follow, 'user', 'following', msg)

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data
