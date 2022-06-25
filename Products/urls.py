from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductsView.as_view()),
    path('<int:product_id>', views.ProductsDetailView.as_view()),
    path('<int:product_id>/quantityupdate', views.UpdateProductQuantity.as_view())
]