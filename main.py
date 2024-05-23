from urllib.parse import urlencode
import spotipy
import base64
import requests
import json
from PIL import Image
import colorsys
from io import BytesIO
from dotenv import load_dotenv
import os
from flask import Flask, request

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_token_from_code(code)
    if token:
        process_spotify_data(token)
        return "Spotify data processed successfully!"
    else:
        return "Failed to obtain access token."

def get_auth_url():
    scopes = "user-top-read"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scopes,
    }
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return url

def get_token_from_code(auth_code):
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def SpotipyAuth(token):
    return spotipy.Spotify(auth=token)

def get_songs_image_url(item):
    return item['album']['images'][0]['url']

def get_songs_image_name(item):
    url = item['album']['images'][0]['url']
    name = item['name']
    list = [url, name]
    return list

def get_list_songs_image_name(result):
    list = []
    for item in result['items']:
        url = get_songs_image_name(item)[0]
        if not url.startswith('http'):
            url = 'https:' + url
        name = get_songs_image_name(item)[1]
        item_list = [url, name]
        list.append(item_list)
    return list

def get_dominant_color(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((150, 150))
    image = image.convert('RGB')
    pixels = list(image.getdata())
    color_counts = {}
    for pixel in pixels:
        color_counts[pixel] = color_counts.get(pixel, 0) + 1
    dominant_color = max(color_counts, key=color_counts.get)
    return dominant_color 

def get_closest_song_with_color(user_top_tracks_urls_name, target_color):
    closest_song = None
    closest_distance = float('inf')
    for track in user_top_tracks_urls_name:
        url = track[0]
        dominant_color = get_dominant_color(url)
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(dominant_color, target_color)) ** 0.5
        if distance < closest_distance:
            closest_distance = distance
            closest_song = track
            name = track[1]
        lista = [url, name]
    return lista

def process_spotify_data(token):
    Spotify = SpotipyAuth(token)
    total_tracks = int(input("Enter number of songs you want displayed: "))
    limit = 20
    list_of_songs = []
    for offset in range(0, total_tracks, limit):
        result = Spotify.current_user_top_tracks(limit, time_range='long_term', offset=offset)
        list_of_songs.extend(get_list_songs_image_name(result))
    rainbow_colors = {
        'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'indigo': (75, 0, 130),
        'violet': (148, 0, 211)
    }
    for color, rgb in rainbow_colors.items():
        closest_song = get_closest_song_with_color(list_of_songs, rgb)
        print(f"{color.capitalize()}: {closest_song[1]} ({closest_song[0]})")

if __name__ == "__main__":
    print("Go to the following URL to authorize the application:")
    print(get_auth_url())
    app.run(port=5000)
