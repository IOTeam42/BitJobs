from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from bargainflow import views

router = DefaultRouter()

router.register(r'commissions', views.CommissionViewSet)
router.register(r'commission-bids', views.CommissionBidViewSet)


urlpatterns = [
    url(r'^',include(router.urls)),
]
