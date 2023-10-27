from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    Предоставляет queryset cо всеми постами
    которые имеют статус Published
    """
    def get_queryset(self):
        return (super().get_queryset()
                .filter(status=Post.Status.PUBLISH))


class Post(models.Model):
    """
    Модель постов в блоге
    """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISH = 'PB', 'Published'

    title = models.CharField(
        verbose_name='Заголовок поста',
        max_length=250
    )
    slug = models.SlugField(
        verbose_name='Slug поста',
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор поста'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        db_table = 'post'
        ordering = ('-publish',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        indexes = (
            models.Index(fields=('-publish',)),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class Comment(models.Model):
    """
    Модель комментариев к постам
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(verbose_name='Имя автора комментария', max_length=80)
    email = models.EmailField(verbose_name='Email автора комментария')
    body = models.TextField(verbose_name='Текс комментария')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'comment'
        ordering = ('created', )
        indexes = (
            models.Index(fields=('created', )),
        )

    def __str__(self):
        return f'Comments by {self.name} on {self.email}'
