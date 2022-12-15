import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import youtube_dl
from decouple import config


os.environ["SPOTIPY_CLIENT_ID"] = config('SPOTIPY_CLIENT_ID')
os.environ["SPOTIPY_CLIENT_SECRET"] = config('SPOTIPY_CLIENT_SECRET')
os.environ["SPOTIPY_REDIRECT_URI"] = config('SPOTIPY_REDIRECT_URI')



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def download_song(track_name):
    data = ytdl.extract_info(track_name, download=True)
    if 'entries' in data:
        # take first item from a playlist
        data = data['entries'][0]
        
        
def create_and_change_dir(dirname):
    directory = dirname
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)
    if not os.path.exists(path): 
        os.mkdir(path)
    os.chdir(path)

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
        
    print("\n\n")
    
    create_and_change_dir("Playlists")
    create_and_change_dir(target_playlist["name"])
    
    for track in tracks:
        print(f"Downloading \'{track}\'...")
        download_song(track)
    
    print("\n\nDone.\n\n")

        
        
if __name__ == '__main__':
    main()