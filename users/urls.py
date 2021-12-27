from django.urls import path
from django.conf.urls import url


# internal
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path('profile/', views.profile, name='profile'),
    path('activate/<uidb64>/<token>/',
        views.activate, name='activate'),
]
