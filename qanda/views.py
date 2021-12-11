from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect
from django.contrib import messages
# internals
from .models import Question
from .forms import AnswerForm

def qanda(request):
    '''Question and Answers index'''
    questions = Question.objects.all()
    context = {
        'questions' : questions
    }
    return render(request, 'qanda/index.html', context)

def question_detail(request, year, month, day, slug):
    def queryset():
        qs = Question.objects.prefetch_related('answers').annotate(
            answer_count=Count('answers'))
        return qs

    question = get_object_or_404(queryset(), slug=slug,
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day
                             )
    # list of answers for this question
    answers = question.answers.filter()
    context = {'question': question,
               'answers': answers,
               'similar_questions': get_similar_questions(question)
               }

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            # Create answer object but don't save to database yet
            new_answer = answer_form.save(commit=False)
            new_answer.question = question
            new_answer.author = request.user
            new_answer.save()
            messages.success(request, _("Your answer has been added"))
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        answer_form = AnswerForm()
        context['answer_form'] = answer_form
    return render(request, 'qanda/detail.html', context)

def get_similar_questions(question: Question):
    # list of similar questions
    question_tags_ids = question.tags.values_list('id', flat=True)
    similar_questions = Question.objects.filter(
        tags__in=question_tags_ids).exclude(id=question.id)
    similar_questions = similar_questions.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-published_date')[:4]
    return similar_questions