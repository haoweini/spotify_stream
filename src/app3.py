import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import spotipy
import streamlit as st

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
scope = spotify_creds['saved_library_scope']
redirect_uri = spotify_creds['saved_library_redirect_url']

def get_token(scope):
    
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    
    return token

all_token = get_token('user-library-read user-read-recently-played user-top-read')

st.text(all_token)


