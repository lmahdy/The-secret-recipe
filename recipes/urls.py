from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_recipe, name='search_recipe'),
]
