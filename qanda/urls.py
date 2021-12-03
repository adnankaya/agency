from django.urls import path

from . import views

app_name = 'qanda'

urlpatterns = [

    path('questions/', views.qanda, name='qanda'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.question_detail, name='question-detail'),
]
