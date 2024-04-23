from django.urls import path
from . import views

urlpatterns = [
    path('', views.TempInfoView.as_view(), name='tempinfo'),
    path('average/<str:period>/', views.AverageTemperatureView.as_view(), name='average_temperature'),
]