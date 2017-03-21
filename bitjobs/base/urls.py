from django.conf.urls import url
from base import views

urlpatterns = [
    url(r'^rejestracja', views.RegisterView.as_view(), name="registration"),
    url(r'^logowanie', views.LoginView.as_view(), name="login"),
]