from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<str:pk>', views.detail_view, name='detail'),
]
