from django.conf import settings
from django.db.models import Prefetch, F, Sum
from django.core.cache import cache
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionsSerializer


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email')),
    )
    serializer_class = SubscriptionsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum(F('price'))).get('total') or 0
            cache.set(settings.PRICE_CACHE_NAME, total_price, timeout=60 * 60)

        response_data = {'result': response.data, 'total': total_price}
        response.data = response_data
        return response