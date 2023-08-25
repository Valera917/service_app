from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription
from services.serializers import SubscriptionsSerializer


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    #
    # def get_queryset(self):
    #     return Subscriptions.objects.filter(user=self.request.user)
