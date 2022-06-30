from re import M
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json


os.environ["SPOTIPY_CLIENT_ID"] = "7489e150d7744a22a259dac64438a44c"
os.environ["SPOTIPY_CLIENT_SECRET"] = "befe11f551954ab8bfd9d8acd925df84"
os.environ["SPOTIPY_REDIRECT_URI"] = "https://github.com/Keatsm/spotifymp3"


def main():
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    

    results = sp.current_user_playlists()
    
    for playlist in results:
        print(playlist)
    

    
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     print(idx, track['artists'][0]['name'], " – ", track['name'])
        
        
if __name__ == '__main__':
    main()