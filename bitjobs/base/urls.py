from django.conf.urls import url, include
from registration.backends.default.views import RegistrationView
from base import views


urlpatterns = [
    url(r'^rejestracja/', views.RegisterView.as_view(),
        name="registration"),
    url(r'^oferta/(?P<id>[0-9]+)$', views.CommissionView.as_view(),
        name="commission-detail"),
    url(r'^oferty/$', views.CommissionDashboardView.as_view(),
        name="commission-dashboard"),
    url(r'^$', views.HomeView.as_view(),
        name="home"),
    url(r'^oferta/', views.CommissionAddView.as_view(),
        name="add-commission"),
    url(r'^500/', views.Error500View.as_view(),
        name="error-500"),
    url(r'^403/', views.Error403View.as_view(),
        name="error-403"),
    url(r'^404/', views.Error404View.as_view(),
        name="error-404"),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts_auth/', include('django.contrib.auth.urls')),
]
