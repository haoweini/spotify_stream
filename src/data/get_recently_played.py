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
scope = spotify_creds['recently_played_scope']
redirect_uri = spotify_creds['recently_played_redirect_url']


sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)


def get_recently_played():

    df_saved_tracks = pd.DataFrame()
    track_list = ''
    played_ts_list = []
    artist_list = []
    title_list = []
    track_url_list = []
    popularity_list = []
    album_cover_list = []
    more_songs = True


    songs = sp.current_user_recently_played(limit=50)
    for song in songs['items']:
        #join track ids to a string for audio_features function
        track_list += song['track']['id'] +','
        #get the time when the song was added
        played_ts_list.append(song['played_at'])
        #get the title of the song
        title_list.append(song['track']['name'])
        #get popularity
        popularity_list.append(song['track']['popularity'])
        # get album cover
        album_cover_url = song['track']['album']['images'][0]['url']
        album_cover_list.append(album_cover_url)
        # get track list
        track_url = song['track']['external_urls']['spotify']
        track_url = track_url.split('/')[-1]
        track_url_list.append(track_url)
        #get all the artists in the song
        artists = song['track']['artists']
        artists_name = ''
        for artist in artists:
            artists_name += artist['name']  + ','
        artist_list.append(artists_name[:-1])
        track_list = ''
        #include timestamp added, title and artists of a song
    df_saved_tracks['song_title'] = title_list
    df_saved_tracks['artists'] = artist_list
    df_saved_tracks['played_at'] = played_ts_list
    df_saved_tracks['album_cover'] = album_cover_list
    df_saved_tracks['popularity'] = popularity_list
    df_saved_tracks['url'] = track_url_list
    
    return df_saved_tracks