from django.urls import path
from . import views

urlpatterns = [
    path('', views.CollectedItemsListView.as_view(), name="listandadd"),
    path('<int:item_id>', views.CollectedItemsDetailView.as_view(), name="Collected Items Details"),
    path('apprentice', views.ApprenticeView.as_view(), name="apprentice")
]
