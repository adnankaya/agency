from django.urls import path

from . import views

app_name = 'qanda'

urlpatterns = [

    path('questions/', views.qanda, name='qanda'),
    path('questions/new-question', views.QuestionCreateView.as_view(), name='new-question'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.question_detail, name='question-detail'),
]
