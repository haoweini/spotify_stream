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
import numpy as np
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
scope = 'user-library-read user-read-recently-played user-top-read'
redirect_uri = spotify_creds['top_artist_redirect_url']


sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)

#####
def get_top_artists():
    df_top_artists = pd.DataFrame()
    artists_list = []
    genres_list = []
    artists_pic_list = []
    popularity_list = []
    artist_url_list = []
    followers_list = []
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    artists = sp.current_user_top_artists()
    
    for artist in artists['items']:
        artists_pic_list.append(artist['images'][0]['url'])
        artists_list.append(artist['name'])
        genres_list.append(artist['genres'][0])
        popularity_list.append(artist['popularity'])
        followers_list.append(artist['followers']['total'])
        artist_url = artist['external_urls']['spotify']
        artist_url = artist_url.split('/')[-1]
        artist_url_list.append(artist_url)

        
    df_top_artists['artist'] = artists_pic_list 
    df_top_artists['name'] = artists_list
    df_top_artists['genere'] = genres_list
    df_top_artists['popularity'] = popularity_list
    df_top_artists['followers'] = followers_list
    df_top_artists['url'] = artist_url_list

    return df_top_artists

#####
def get_top_tracks():

    df_saved_tracks = pd.DataFrame()
    track_list = ''
    artist_list = []
    title_list = []
    track_url_list = []
    popularity_list = []

    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    songs = sp.current_user_top_tracks(limit=50)
    for song in songs['items']:
        #join track ids to a string for audio_features function
        track_list += song['id'] +','
        
        #get the title of the song
        title_list.append(song['name'])
        #get popularity
        popularity_list.append(song['popularity'])
        # get track list
        track_url = song['external_urls']['spotify']
        track_url = track_url.split('/')[-1]
        track_url_list.append(track_url)
        #get all the artists in the song
        artists = song['artists']
        artists_name = ''
        for artist in artists:
            artists_name += artist['name']  + ','
        artist_list.append(artists_name[:-1])
        track_list = ''
        #include timestamp added, title and artists of a song
    df_saved_tracks['song_title'] = title_list
    df_saved_tracks['artists'] = artist_list
    df_saved_tracks['popularity'] = popularity_list
    df_saved_tracks['url'] = track_url_list
    
    return df_saved_tracks

####
def get_related_artists(artist_name):
    
    df_related_artists = pd.DataFrame()
    artists_list = []
    genres_list = []
    artists_pic_list = []
    popularity_list = []
    artist_url_list = []
    followers_list = []
    
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    artist_id = sp.search(artist_name)
    artist_url = artist_id['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
    artist_url = artist_url.split('/')[-1]
    
    artists = sp.artist_related_artists(artist_url)
    
    for artist in artists['artists']:
        artists_list.append(artist['name'])
        #genres_list.append(artist['genres'][0])
        popularity_list.append(artist['popularity'])
        followers_list.append(artist['followers']['total'])
        artist_url = artist['external_urls']['spotify']
        artist_url = artist_url.split('/')[-1]
        artist_url_list.append(artist_url)

        
    
    df_related_artists['name'] = artists_list
    #df_related_artists['genere'] = genres_list
    df_related_artists['popularity'] = popularity_list
    df_related_artists['followers'] = followers_list
    df_related_artists['url'] = artist_url_list
    df_related_artists = df_related_artists.sort_values(by=['popularity','followers'], ascending=[False,False])
    
    return df_related_artists

#####3
def get_top_artists_tracks_features(artist_name):
    
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    artist_id = sp.search(q=artist_name, type="artist", limit=10)
    artist_url = artist_id['artists']['items'][0]['external_urls']['spotify']
    artist_url = artist_url.split('/')[-1]
    
    songs = sp.artist_top_tracks(artist_url)
    
    df_artist_top_tracks = pd.DataFrame()
    track_name = []

    for song in songs['tracks']:
        #join track ids to a string for audio_features function
        track_name.append(song['name'])
        track_url = song['external_urls']['spotify'].split('/')[-1]
        track_features = sp.audio_features(track_url)
        df_temp = pd.DataFrame(track_features)
        df_artist_top_tracks = df_artist_top_tracks.append(df_temp)
        
    df_artist_top_tracks['track'] = track_name
    df_artist_top_tracks['artist'] = artist_name
    df_artist_top_tracks = df_artist_top_tracks[['artist','track', 'acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'tempo']]
    df_artist_top_tracks = df_artist_top_tracks.rename(columns={'tempo': 'BPM'})
    
    return df_artist_top_tracks


####3
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def draw_feature_plot(df):
    
    df[['BPM']] = NormalizeData(df[['BPM']])

    df = df.groupby(['artist'])['track', 'acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM'].mean().reset_index()
    df = df[['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM']]

    fig = px.line_polar(df, r=df.loc[0].values, theta=df.columns, range_r = [0,1.0], line_close=True)
    fig.update_layout(height=500, width=500)
    fig.update_traces(fill='toself')
    
    return fig

###
def search_random_artist(artist):
    
    df_artist = pd.DataFrame()
    followers = []
    popularity = []
    
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    artist_id = sp.search(q=artist, type="artist", limit=10)
    artist_url = artist_id['artists']['items'][0]['external_urls']['spotify']
    artist_url = artist_url.split('/')[-1]
    artist_info = sp.artist(artist_url)
    
    followers.append(artist_info['followers']['total'])
    popularity.append(artist_info['popularity'])
    
    df_artist['followers'] = followers
    df_artist['url'] = artist_url
    df_artist['popularity'] = popularity
    
    return df_artist