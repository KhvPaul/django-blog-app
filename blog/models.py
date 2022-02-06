import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Blogger(AbstractUser):

    bio = models.TextField(max_length=1000, help_text='Blogger biography', blank=True)
    profile_picture = models.ImageField(null=True, blank=True, default='unknown_user.jpg')

    class Meta:
        verbose_name_plural = 'Bloggers'

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])


class Blog(models.Model):
    blogger = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text='Blog title')
    content = models.TextField(max_length=3000, help_text='Blog content')
    post_date = models.DateTimeField(auto_now_add=True)
    is_posted = models.BooleanField(default=False)
    publication_request = models.BooleanField(null=True)
    notified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def get_date(self):
        return f'{self.post_date.strftime("%b")} {self.post_date.day}, {self.post_date.year}'

    def get_formatted_post_date(self):
        if self.post_date.day == datetime.datetime.now().day:
            return f"{self.post_date.strftime('%H:%M:%S')}"
        if self.post_date.day == datetime.datetime.now().day - 1:
            return f"tomorrow at {self.post_date.strftime('%H:%M:%S')}"
        if self.post_date.day - datetime.datetime.now().day - 1 <= 7:
            return f"{self.post_date.day - datetime.datetime.now().day}" \
                   f" days ago at {self.post_date.strftime('%H:%M:%S')}"[1:]
        else:
            return f"{self.post_date.strftime('%Y-%m-%d %H:%M:%S')}"


class Comment(models.Model):
    blogger = models.CharField(max_length=50, default='Anonymous')
    content = models.TextField(max_length=1000, help_text='Enter the comment about the blog here')
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    is_posted = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content}'

    def get_date(self):
        return f'{self.post_date.strftime("%b")} {self.post_date.day}, {self.post_date.year}'
