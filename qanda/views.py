from django.shortcuts import render

# internals
from .models import Question

def qanda(request):
    '''Question and Answers index'''
    questions = Question.objects.all()
    context = {
        'questions' : questions
    }
    return render(request, 'qanda/index.html', context)