import markdown
from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
# internals
from ..models import Question

register = template.Library()


@register.simple_tag
def total_questions():
    return Question.published.count()


@register.inclusion_tag('qanda/latest_questions.html')
def show_latest_questions(count=5):
    latest_questions = Question.objects.order_by('-published_date')[:count]
    return {'latest_questions': latest_questions}


@register.simple_tag
def get_most_answered_questions(count=5):
    return Question.objects.annotate(
        total_answers=Count('answers')).order_by('-total_answers')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
