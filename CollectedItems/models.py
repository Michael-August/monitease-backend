from tabnanny import verbose
from django.db import models

# Create your models here.

class Apprentice(models.Model):
    apprenticeName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.apprenticeName

class CollectedItems(models.Model):
    itemCollected = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    totalPrice = models.IntegerField()
    collectedFrom = models.CharField(max_length=100)
    collectedBy = models.ForeignKey(Apprentice, related_name="whoPicked", on_delete=models.CASCADE)
    havePaid = models.BooleanField(default=False)
    dateCollected = models.DateTimeField(auto_now_add=True, auto_now=False)
    datePaid = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Collected Items'

    def __str__(self):
        return self.itemCollected

    def save(self, *args, **kwargs):
        self.totalPrice = self.rate * self.quantity
        super(CollectedItems, self).save(*args, **kwargs)
