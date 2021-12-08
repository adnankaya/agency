from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


# internal
from core.utils import generate_slug
from publish.models import Publish
from core.models import Base
from django.core.validators import MaxValueValidator, MinValueValidator


class Question(Publish):
    text = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=250,
                            unique_for_date='published_date')
    rate = models.PositiveSmallIntegerField(default=1,
                                            validators=[
                                                MaxValueValidator(5),
                                                MinValueValidator(1)
                                            ])

    class Meta:
        db_table = 't_questions'

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('qanda:question-detail',
                       args=[
                           self.published_date.year,
                           self.published_date.month,
                           self.published_date.day,
                           self.slug
                       ])

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.text)
        super(Question, self).save()


class Answer(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="%(app_label)s_%(class)s_related")
    body = RichTextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')

    class Meta:
        db_table = 't_answers'
        ordering = ('-created_date',)
