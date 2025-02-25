import requests
from io import BytesIO
from PIL import Image
from colorthief import ColorThief
import numpy as np

def get_songs_image_name(item):
    """
    Extract the album image URL and song name from a Spotify track item.
    """
    url = item['album']['images'][0]['url']
    name = item['name']
    return url, name

def get_list_songs_image_name(result):
    """
    Given a Spotify API result, return a list of [url, name] for each song.
    """
    songs = []
    for item in result.get('items', []):
        url, name = get_songs_image_name(item)
        # Ensure the URL is complete.
        if not url.startswith('http'):
            url = 'https:' + url
        songs.append([url, name])
    return songs

def get_dominant_color(url, resize_factor=0.5, quality=1):
    """
    Downloads the image from the given URL, resizes it using PIL to speed up processing,
    and then uses ColorThief to get the dominant color.
    
    Parameters:
      - url: URL of the image.
      - resize_factor: Factor to reduce the image size (0.5 will reduce both dimensions by 50%).
      - quality: Quality setting for ColorThief (lower numbers are slower but more accurate).
    
    Returns:
      A tuple (R, G, B) representing the dominant color.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        # Fallback color in case of an error.
        return (0, 0, 0)
    
    # Open the image using PIL.
    image = Image.open(BytesIO(response.content))
    
    # Calculate new dimensions based on the resize factor.
    new_width = max(1, int(image.width * resize_factor))
    new_height = max(1, int(image.height * resize_factor))
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Save the resized image to a BytesIO object.
    image_io = BytesIO()
    resized_image.save(image_io, format='JPEG')
    image_io.seek(0)
    
    # Use ColorThief on the resized image.
    color_thief = ColorThief(image_io)
    dominant_color = color_thief.get_color(quality=quality)
    return dominant_color

def hex_to_rgb(hex_color):
    """
    Convert a hex color string (e.g. "#ff0000") to an RGB tuple.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    """
    Compute the Euclidean distance between two colors (given as RGB tuples).
    """
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

def get_top_n_songs_with_color(songs, target_color, n=100):
    """
    Given a list of songs (each song is a [url, name] list), this function computes each song’s
    dominant color (using a resized image with ColorThief) and compares it to the target_color.
    It then returns the top n songs whose dominant colors are closest to the target_color.
    """
    songs_with_distance = []
    for song in songs:
        url, name = song
        dominant_color = get_dominant_color(url)
        distance = color_distance(dominant_color, target_color)
        songs_with_distance.append((song, distance))
    
    # Sort songs by distance in ascending order (closest first).
    songs_with_distance.sort(key=lambda tup: tup[1])
    return [song for song, dist in songs_with_distance[:n]]