from django.urls import path
# internals
from . import views

app_name = 'company'

urlpatterns = [
    path('services/', views.services_list, name='services-list'),
    path('services/<slug:slug>/', views.service_detail, name='service-detail'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
