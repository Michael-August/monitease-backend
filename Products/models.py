from django.db import models

# Create your models here.
default = 50

class Products(models.Model):
    item_name = models.CharField(max_length=80)
    quantity = models.IntegerField()
    total_added = models.IntegerField()
    percent = models.IntegerField(default=0)
    restocklevel = models.IntegerField()
    dateadded = models.DateField(auto_now_add=True)
    dateupdated = models.DateField(auto_now=True)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        # self.total_added = self.quantity
        self.percent = self.quantity/default * 100
        super(Products, self).save(*args, **kwargs)

