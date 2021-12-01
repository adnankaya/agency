from django.urls import path

from . import views

app_name = 'qanda'

urlpatterns = [

path('', views.qanda, name='qanda')
]