from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


# Create your views here.


def index(request):
    trans = _('Hello')
    msg = translate(msg='Hello', language='tr')
    context = {
        'trans': trans,
        'msg': msg
    }
    return render(request, 'home/index.html', context=context)


def translate(msg, language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext(msg)
    finally:
        activate(cur_language)
    return text
