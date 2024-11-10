from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL for the contact form
    path('search/', views.search_recipe, name='search_recipe'),#this is the url that will be used to search for recipes
    path('map/', views.map_view, name='map_view'),  #this is the url that will be used to display the map
    path('summarize_audio/', views.summarize_audio, name='summarize_audio'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/top-tracks/', views.top_tracks, name='top_tracks'),
     path('word-lookup/', views.word_lookup, name='word_lookup'),  # Render the form page
    path('word-lookup-data/', views.word_lookup_data, name='word_lookup_data'),  # AJAX endpoint for JSON data

]
