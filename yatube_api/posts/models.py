from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Название группы.', max_length=200)
    slug = models.SlugField(verbose_name='Отображение в URL строке, '
                            'при открытии страницы записей группы.',
                            unique=True)
    description = models.TextField(verbose_name='Описание группы.')

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор поста',
                               on_delete=models.CASCADE,
                               related_name='posts')
    text = models.TextField(verbose_name='Содержание поста')
    group = models.ForeignKey(Group, verbose_name='Группа поста',
                              blank=True,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='posts')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/images/',
        default=None
    )
    pub_date = models.DateTimeField(verbose_name='Дата создания поста',
                                    auto_now_add=True)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Пост для комментария',
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор поста',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(verbose_name='Дата создания комментария',
                                   auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='Подписчик',
                             on_delete=models.CASCADE,
                             related_name='follower')
    following = models.ForeignKey(User, verbose_name='Автор',
                                  on_delete=models.CASCADE,
                                  related_name='following')
