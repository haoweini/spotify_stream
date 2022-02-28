import configparser
import json
import spotipy
import spotipy.util as util
import pandas as pd
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import bamboolib
import streamlit as st
import requests
from data.get_saved_library import  connect_to_spotify_api 

import warnings
warnings.filterwarnings("ignore")

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
scope = spotify_creds['top_artist_scope']
redirect_uri = spotify_creds['top_artist_redirect_url']


sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)

def get_top_artists():
    df_top_artists = pd.DataFrame()
    artists_list = []
    genres_list = []
    artists_pic_list = []
    popularity_list = []
    artist_url_list = []
    artists = sp.current_user_top_artists()
    
    for artist in artists['items']:
        artists_pic_list.append(artist['images'][0]['url'])
        artists_list.append(artist['name'])
        genres_list.append(artist['genres'][0])
        popularity_list.append(artist['popularity'])
        artist_url = artist['external_urls']['spotify']
        artist_url = artist_url.split('/')[-1]
        artist_url_list.append(artist_url)

        
    df_top_artists['artist'] = artists_pic_list 
    df_top_artists['name'] = artists_list
    df_top_artists['genere'] = genres_list
    df_top_artists['popularity'] = popularity_list
    df_top_artists['url'] = artist_url_list

    return df_top_artists