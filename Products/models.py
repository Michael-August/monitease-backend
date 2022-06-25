from django.db import models

# Create your models here.

class Products(models.Model):
    item_name = models.CharField(max_length=80)
    quantity = models.IntegerField()
    restocklevel = models.IntegerField()
    dateadded = models.DateField(auto_now_add=True)
    dateupdated = models.DateField(auto_now=True)

    def __str__(self):
        return self.item_name
