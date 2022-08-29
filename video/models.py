# from tinymce.models import HTMLField
from django.db import models
# from tinymce import models as tinymce_models

from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField

User = get_user_model()


class VideoView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_user')
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self) -> str:
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    country = CountryField(default='togo')

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    video = models.ForeignKey(
        'Video', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Video(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    video_url = models.CharField(max_length=300, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='video_category')
    featured = models.BooleanField()
    status = models.CharField(choices=STATUS_CHOICES, default='published', max_length=10)
    is_on_top = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('video-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('video-delete', kwargs={
            'pk': self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(video=self).count()

    @property
    def view_count(self):
        return VideoView.objects.filter(video=self).count()
