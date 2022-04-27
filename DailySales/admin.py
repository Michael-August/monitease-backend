from django.contrib import admin

from DailySales.models import DailySales, ItemSold

# Register your models here.

admin.site.register(DailySales)
admin.site.register(ItemSold)
