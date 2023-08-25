from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from services.views import SubscriptionsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'api/subscriptions', SubscriptionsViewSet)

urlpatterns += router.urls
