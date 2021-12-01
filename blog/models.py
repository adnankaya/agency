from django.db import models
from django.urls import reverse
# internal
from core.utils import generate_slug
from publish.models import Publish
from .managers import PublishedManager

class Post(Publish):
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    body = models.TextField()

    slug = models.CharField(max_length=250,
                            unique_for_date='published_date')

    status = models.CharField(max_length=10, choices=STATUS_CHOISES,
                              default='draft')

    published = PublishedManager()

    class Meta:
        db_table = 't_blog'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.published_date.year,
                           self.published_date.month,
                           self.published_date.day,
                           self.slug
                       ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    made_by = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 't_comment'
        ordering = ('created',)

    def __str__(self):
        return f"Comment by {self.made_by} on {self.post}"
