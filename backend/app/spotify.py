import base64
import requests
import spotipy
from urllib.parse import urlencode
from app.image_utils import get_list_songs_image_name, get_top_n_songs_with_color, hex_to_rgb

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

def get_auth_url():
    scopes = "user-top-read playlist-modify-public"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scopes,
    }
    return "https://accounts.spotify.com/authorize?" + urlencode(params)

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

def process_spotify_data(token, total_tracks, target_color, top_n=100):
    """
    Retrieve the user's top tracks (up to total_tracks) and then return
    the top_n songs whose album image dominant colors are closest to target_color.
    target_color should be provided as a hex string (e.g. "#ff0000").
    """
    spotify_client = SpotipyAuth(token)
    limit = 50
    songs_list = []
    
    for offset in range(0, total_tracks, limit):
        result = spotify_client.current_user_top_tracks(limit, time_range='long_term', offset=offset)
        songs_list.extend(get_list_songs_image_name(result))
    
    target_rgb = hex_to_rgb(target_color)
    top_songs = get_top_n_songs_with_color(songs_list, target_rgb, top_n)
    
    # Format the result as a list of dictionaries.
    result = []
    for song in top_songs:
        url, name = song
        result.append({"name": name, "image_url": url})
    return result
