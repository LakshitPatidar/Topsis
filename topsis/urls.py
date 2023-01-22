from unicodedata import name
from django.urls import path
from topsis import views

urlpatterns = [
    path('', views.topsis_view, name='index'),
]