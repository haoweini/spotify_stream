import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy
import configparser
import json

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)
    

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
redirect_uri = spotify_creds['top_artist_redirect_url']

def get_token(scope):
    
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    
    return token

def save_token():
    all_token = get_token('user-library-read user-read-recently-played user-top-read ')
    #recently_played_token = get_token('user-read-recently-played')
    #top_artist_token = get_token('user-top-read')
    
    with open(r"../data/raw/spotify_tokens.json",
        "w") as fp:
        json.dump({"all_access_token": all_token}, fp)

save_token()