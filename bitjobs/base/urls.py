from base import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^rejestracja/', views.RegisterView.as_view(),
        name="registration"),
    url(r'^oferta/(?P<pk>[0-9]+)$', views.CommissionView.as_view(),
        name="commission-detail"),
    url(r'^oferta/(?P<pk>[0-9]+)/wybierz/(?P<bid_id>[0-9]+)$', views.commission_choose,
        name='commission-choose'),
    url(r'^oferty/$', views.CommissionDashboardView.as_view(),
        name="commission-dashboard"),
    url(r'^oferty-uzytkownika/$', views.CommissionUserView.as_view(),
        name="commission-user-dashboard"),
    url(r'^$', views.HomeView.as_view(),
        name="home"),
    url(r'^oferta/$', views.CommissionAddView.as_view(),
        name="add-commission"),
    url(r'^bid/', views.CommissionBidView.as_view(),
        name="commission-bid"),
    url(r'^oferta/(?P<commission_id>[0-9]+)/akceptuj$', views.commission_accept_work,
        name="commission-accept"),
    url(r'^500/', views.Error500View.as_view(),
        name="error-500"),
    url(r'^403/', views.Error403View.as_view(),
        name="error-403"),
    url(r'^404/', views.Error404View.as_view(),
        name="error-404"),
    url(r'^uzytkownik/(?P<pk>[0-9]+)$', views.CustomerView.as_view(),
        name="user-detail"),
    url(r'^opinie/$', views.OpinionUserView.as_view(),
        name="customer-opinions"),
    #url(r'^opiniuj/(?P<pk>[0-9]+)$', views.OpinionAddView.as_view(),
    #    name="opinion-add"),
    url(r'^opiniuj/$', views.OpinionAddView.as_view(),
        name="opinion-add"),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts_auth/', include('django.contrib.auth.urls')),
]
