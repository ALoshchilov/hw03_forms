from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Группу"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )


    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            f'Author: {self.author} Pub_date: {self.pub_date} '
            f'Group: {self.group} Text: {self.text[:50]}...'
        )
