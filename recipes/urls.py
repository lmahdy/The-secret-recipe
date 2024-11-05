from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_recipe, name='search_recipe'),
    path('map/', views.map_view, name='map_view'),  # Add this line
]
