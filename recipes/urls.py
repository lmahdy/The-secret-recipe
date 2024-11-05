from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_recipe, name='search_recipe'),#this is the url that will be used to search for recipes
    path('map/', views.map_view, name='map_view'),  #this is the url that will be used to display the map
    path('summarize_audio/', views.summarize_audio, name='summarize_audio')

]
