from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# internal
from core.utils import generate_slug
from publish.models import Publish
from core.models import Base
from django.core.validators import MaxValueValidator, MinValueValidator


class Question(Publish):
    text = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(default=1,
                                            validators=[
                                                MaxValueValidator(5),
                                                MinValueValidator(1)
                                            ])

    class Meta:
        db_table = 't_questions'

    def __str__(self):
        return self.text


class Answer(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="%(app_label)s_%(class)s_related")
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')

    class Meta:
        db_table = 't_answers'
        ordering = ('-created_date',)
