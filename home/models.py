from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    replay = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', null=True, blank=True)
    is_replay = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}  --  {self.body[:30]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def __str__(self):
        return f'{self.user} like {self.post}'
