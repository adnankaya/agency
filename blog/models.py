from django.db import models
from django.urls import reverse
from core.models import Base
# internal
from core.utils import generate_slug
from publish.models import Publish
from .managers import DraftManager, PublishedManager
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _



class Post(Publish):
    STATUS_CHOISES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    title = models.CharField(max_length=250)
    body = RichTextField()

    slug = models.CharField(max_length=250,
                            unique_for_date='published_date')

    status = models.CharField(max_length=10, choices=STATUS_CHOISES,
                              default='draft')

    published = PublishedManager()
    draft = DraftManager()

    class Meta:
        db_table = 't_blog'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       args=[
                           self.published_date.year,
                           self.published_date.month,
                           self.published_date.day,
                           self.slug
                       ])


class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    made_by = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 't_comment'
        ordering = ('created_date',)

    def __str__(self):
        return f"Comment by {self.made_by} on {self.post}"
