import os
import requests
from django.shortcuts import render
from django.conf import settings  # Make sure to import settings
from django.core.files.storage import default_storage

def search_recipe(request):#this function is called when the user searches for a recipe
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



def map_view(request):#this function is called when the user wants to view the map
    print("Map view called") 
    return render(request, 'recipes/map.html', {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})#this returns the map.html template with the Google Maps API key

def summarize_audio(request):
    summary = ""
    if request.method == 'POST':# this means that the user has submitted the form
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            file_path = default_storage.save('uploads/' + audio_file.name, audio_file)#this means that the file is saved in the uploads folder in the media directory
            # Absolute path to the file for upload to Deepgram
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)#this means that the full path to the file is the media root + the file path in our case its media/uploads/filename
            
            # Prepare headers and data for the Deepgram API
            headers = {
                'Authorization': f'Token {settings.DEEPGRAM_API_KEY}',
                'Content-Type': 'audio/wav'  # Change as per the file type
            }

            with open(full_path, 'rb') as f:
                response = requests.post(
                    'https://api.deepgram.com/v1/listen?summarize=v2',
                    headers=headers,
                    data=f
                )#this means that we are sending a post request to the Deepgram API with the audio file
                data = response.json()#this means that we are converting the response to JSON format
                summary = data.get('results', {}).get('summary', {}).get('short', "No summary available.")#this means that we are getting the summary from the response
            
            # Clean up the uploaded file if desired
            default_storage.delete(file_path)

    return render(request, 'recipes/summarize_audio.html', {'summary': summary})

