import os
import requests
from django.shortcuts import render

def search_recipe(request):
    query = request.GET.get('query')  # Get the dish name from the user input
    app_id = os.getenv('RECIPE_APP_ID')
    app_key = os.getenv('RECIPE_APP_KEY')
    api_url = os.getenv('RECIPE_API_URL')

    # Check if the query parameter is provided
    if query:
        # Make a request to the Edamam API with the dish name and credentials
        response = requests.get(
            api_url,
            params={
                'type': 'public',   # This is required by Edamam's API
                'q': query,
                'app_id': app_id,
                'app_key': app_key
            }
        )
        # Convert the API response to JSON format
        data = response.json()
        # Extract recipes or return an empty list if none are found
        recipes = data.get('hits', [])  # `hits` contains the list of recipes
    else:
        recipes = []

    return render(request, 'recipes/search_results.html', {'recipes': recipes, 'query': query})
