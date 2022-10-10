#made by Femijkf and TheVideoDude
import requests
import time
import spotipy
import spotipy.util as util
from cred import *
from spotipy.oauth2 import SpotifyOAuth
import json

from pprint import pprint


ACCESS_TOKEN  = util.prompt_for_user_token(
        #find your Spotify username in account settings
        username= "your_spotify_username",
        scope= "user-read-playback-state playlist-modify-public user-modify-playback-state",
        client_id=client_ID,
        client_secret=client_SECRET,
        redirect_uri=redirect_URI)

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_PAUSE_TRACK_URL = 'https://api.spotify.com/v1/me/player/devices'

def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()
    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    device_name = json_resp['device']['name']

    uri = json_resp['item']['uri']
    now= time.gmtime()
    current_time = time.asctime(now)

    progression = ((json_resp['progress_ms'])/1000)
    current_track_info = {
        #"id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "device_name": device_name,
        "link": link,
        "progression": progression,
        "current_time": current_time,
        "uri": uri
    }

    return (uri, track_name)

scope = 'playlist-modify-public'
#find your Spotify username in account settings
username = 'your_spotfiy_username'

token = SpotifyOAuth(scope=scope, username=username, client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_URI)
spotifyObject = spotipy.Spotify(auth_manager=token)

#create the playlist
playlist_name = input("Name your Playlist: ")
playlist_description = input("Describe your Playlist: ")

spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

#Find the new Playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#user_input = get_current_track(ACCESS_TOKEN) #input("Enter a song: ")
list_of_songs = []
user_quit= 'n'

while user_quit != 'y':
    song_uri, track_name = get_current_track(ACCESS_TOKEN)
    current_song = []
    if song_uri in list_of_songs:
        ()
    else:
        list_of_songs.append(song_uri)
        current_song.append(song_uri)
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=current_song)
    print(track_name)
