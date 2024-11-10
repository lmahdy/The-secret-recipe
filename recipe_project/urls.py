"""
URL configuration for recipe_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recipes import views as recipe_views  # Import the home view from the recipes app


urlpatterns = [
     path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),# this means that all the urls that start with recipes/ will be handled by the recipes app
    path('', recipe_views.home, name='home'),# this is the home page
    path('notes/', include('notes.urls')),  # Add this line to include notes URLs
]

