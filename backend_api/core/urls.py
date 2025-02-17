from django.urls import path
from . import views


urlpatterns = [
    path('vendors/', views.VendorList.as_view()),
]
