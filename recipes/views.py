import os
import requests
import base64
from django.shortcuts import redirect,render
from django.conf import settings  # Make sure to import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse


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



def index(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Compose the email
        subject = f"Message from {name}"  # Email subject
        body = f"Message: {message}\n\nFrom: {name}\nEmail: {email}"  # Email body
        
        # Send the email
        send_mail(
            subject,          # Subject
            body,             # Message body
            settings.EMAIL_HOST_USER,  # From email (your email)
            [email],          # To email (receiver's email)
            fail_silently=False  # Whether to fail silently or raise an exception
        )

        return render(request, 'recipes/index.html', {'message': 'Your message has been sent!'})
    
    return render(request, 'recipes/index.html')




def spotify_login(request):
    scope = "user-top-read"
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope={scope}"
    )
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_str.encode("utf-8")
    auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {auth_b64}"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    access_token = response_data.get("access_token")

    # Store access token in session for later use
    request.session["access_token"] = access_token
    return redirect(reverse('top_tracks'))

def top_tracks(request):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect('spotify_login')

    # Fetch top tracks from Spotify API
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me/top/tracks?limit=6", headers=headers)
    tracks_data = response.json().get("items", [])

    # Simplify data for display in the template
    tracks = [
        {
            "name": track["name"],
            "artist": ", ".join(artist["name"] for artist in track["artists"]),
            "album": track["album"]["name"],
            "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
        }
        for track in tracks_data
    ]

    return render(request, 'recipes/top_tracks.html', {"tracks": tracks})


