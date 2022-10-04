from ctypes.wintypes import tagRECT
from re import M
from unicodedata import name
from xml.dom.minidom import TypeInfo
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import pytube
from decouple import config


os.environ["SPOTIPY_CLIENT_ID"] = config('SPOTIPY_CLIENT_ID')
os.environ["SPOTIPY_CLIENT_SECRET"] = config('SPOTIPY_CLIENT_SECRET')
os.environ["SPOTIPY_REDIRECT_URI"] = config('SPOTIPY_REDIRECT_URI')





def main():

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

    results = sp.current_user_playlists()

        
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])

    
    for playlist in playlists:
        print(playlist["name"])
        
        
    target_playlist = None
    while target_playlist is None:
        playlist_name = input("Select a playlist: ")
        
        for playlist in playlists:
            if playlist["name"] == playlist_name:
                target_playlist = playlist
                
        try: target_playlist
        except NameError: target_playlist = None
    
    
    playlist = target_playlist
    
    
    tracks = []
    
    result = sp.playlist_tracks(playlist["id"])
    for item in result["items"]:
        track_string = ""
        for artist in item["track"]["artists"]:
            artist_name = artist["name"]
            track_string += f"{artist_name} "
        
        track_name = item["track"]["name"]
        
        track_string += f"- {track_name}"
        
        tracks.append(track_string)
        
    print(tracks)
    
    
    


        
        
if __name__ == '__main__':
    main()