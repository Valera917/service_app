from django.core.validators import MaxValueValidator
from django.db import models

from services.tasks import set_price


class Service(models.Model):
    name = models.CharField(max_length=100)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):

        if self.__full_price != self.full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    play_type = models.CharField(max_length=10, choices=PLAN_TYPES)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100),
                                                   ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_discount_percent = self.discount_percent

    def save(self, *args, **kwargs):

        if self._original_discount_percent != self.discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.play_type} - {self.discount_percent}%'


class Subscription(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'
