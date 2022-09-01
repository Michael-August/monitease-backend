from django.db import models
from Products.models import Products

# Create your models here.

PAYMENT_METHOD = (
    ('CASH', 'cash'),
    ('TRANSFER', 'transfer'),
)


class DailySales(models.Model):   
    customername = models.CharField(max_length=100)
    itemsold = models.ForeignKey(Products, related_name="soldItem", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    totalprice = models.IntegerField(default=0)
    datesold = models.DateField(auto_now_add=True, auto_now=False)
    paymentmethod = models.CharField(max_length=40, choices=PAYMENT_METHOD, default=PAYMENT_METHOD[0][0])
    havepaid = models.BooleanField(default=False)
    datepaid = models.DateField(null=True)
    dateupdated = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Daily Sales'


    def __str__(self):
        return self.customername

    def save(self, *args, **kwargs):
        self.totalprice = self.rate * self.quantity
        super(DailySales, self).save(*args, **kwargs)

