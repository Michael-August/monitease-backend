from django.urls import path
from . import views

urlpatterns = [
    path('', views.DailySalesListView.as_view(), name='salesview'),
    path('<int:sales_id>', views.DailySalesDetailView.as_view(), name='salescreateview'),
    path('products', views.ProductsView.as_view(), name='itemsview'),
    path('filteredReport', views.SalesFilteredReportView.as_view(), name='report'),
    path('report', views.SalesReportView.as_view(), name='report'),
]

