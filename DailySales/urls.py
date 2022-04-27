from django.urls import path
from . import views

urlpatterns = [
    path('', views.DailySalesListView.as_view(), name='salesview'),
    path('<int:sales_id>', views.DailySalesDetailView.as_view(), name='salescreateview'),
    path('items', views.ItemsSoldView.as_view(), name='itemsview'),
]

