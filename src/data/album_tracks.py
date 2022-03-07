import configparser
import json
import spotipy
import spotipy.util as util
import pandas as pd
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import bamboolib
import numpy as np
from data.get_saved_library import  connect_to_spotify_api 
import streamlit as st

import warnings
warnings.filterwarnings("ignore")

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
scope = 'user-library-read user-read-recently-played user-top-read'
redirect_uri = spotify_creds['saved_library_redirect_url']
#token = spotify_token['all_access_token']

sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)

def search_artist_album(artist_NAME):
    df_album = pd.DataFrame()

    album_name = []
    album_url = []
    album_date = []
    album_type = []
    album_group = []
    num_tracks = []

    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    artist_id = sp.search(q=artist_NAME, type="artist", limit=10)
    artist_url = artist_id['artists']['items'][0]['external_urls']['spotify']
    artist_url = artist_url.split('/')[-1]
    artist_name = artist_id['artists']['items'][0]['name']
    
    results = sp.artist_albums(artist_url, album_type='single,album', country='US')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in albums:
        album_name.append(album['name'])
        url = album['external_urls']['spotify']
        url = url.split('/')[-1]
        album_url.append(url)
        album_date.append(album['release_date'])
        album_type.append(album['album_type'])
        album_group.append(album['album_group'])
        num_tracks.append(album['total_tracks'])

    
    df_album['name'] = album_name
    df_album['url'] = album_url
    df_album['release_date'] = album_date
    df_album['type'] = album_type
    df_album['group'] = album_group
    df_album['total_tracks'] = num_tracks
    # Delete Remix Songs
    #artist_remix = 
    #df_album = df_album.loc[~df_album['name'].str.contains('remix', case=False, regex=False, na=False)]
    # Delete songs at same day 
    
    return df_album

def find_album_tracks(album_url):
    
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    album_tracks = sp.album_tracks(album_url)

    df_album_tracks = pd.DataFrame()

    track_name = []
    track_url = []
    track_date = []
    artist_list = []
    songs = album_tracks['items']

    while album_tracks['next']:
        album_tracks = sp.next(album_tracks)
        songs.extend(album_tracks['items'])

    for song in songs:
        track_name.append(song['name'])
        url = song['external_urls']['spotify']
        url = url.split('/')[-1]
        track_url.append(url)
        #all_artists.append(artist_list)

    df_album_tracks['track'] = track_name
    df_album_tracks['url'] = track_url
    #df_album_tracks['artists'] = artist_list
    
    return df_album_tracks

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def find_all_tracks_features(album, artist_NAME):
    sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)
    df_all_tracks = []

    for i in range(len(album)):
        #print(i)
        album_url = album.iloc[i]['url']
        df_tracks = find_album_tracks(album_url)
        df_tracks['release_date'] = album.iloc[i]['release_date']
        df_tracks['ablum'] = album.iloc[i]['name']
        df_all_tracks.append(df_tracks)

    df_all_tracks = pd.concat(df_all_tracks)
    
    df_tracks = []

    for i in range(len(df_all_tracks)):
        track_url = df_all_tracks.iloc[i]['url']
        track_name = df_all_tracks.iloc[i]['track']
        track_date = df_all_tracks.iloc[i]['release_date']
        album_name = df_all_tracks.iloc[i]['ablum']
        #Audio Features
        track_features = sp.audio_features(track_url)
        popularity = sp.track(track_url)['popularity']
        df_track = df_all_tracks[df_all_tracks['url'] == track_url]
        df_temp = pd.DataFrame(track_features)
        df_temp = df_temp[['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'tempo']]
        df_temp = df_temp.rename(columns={'tempo': 'BPM'})
        # Normalize BPM
        #df_temp[['BPM']] = NormalizeData(df_temp[['BPM']])
        
        df_temp['track'] = track_name
        df_temp['album'] = album_name
        df_temp['release date'] = track_date
        df_temp['url'] = track_url
        df_temp['popularity'] = popularity
        #Artists
        song = sp.track(track_url)
        artists = song['artists']
        artist_list = []
        artists_name = ''
        for artist in artists:
            artists_name += artist['name']  + ','
        artist_list.append(artists_name[:-1])
        df_temp['artists'] = artist_list

        df_tracks.append(df_temp)

    df_tracks = pd.concat(df_tracks)
    # select artists 
    df_tracks = df_tracks.loc[df_tracks['artists'].str.contains(artist_NAME, case=False, regex=False, na=False)]
    # drop remix not by artist
    df_tracks = df_tracks.loc[(df_tracks['track'].str.contains(artist_NAME, case=False, regex=False, na=False)) | (~df_tracks['track'].str.contains('mix', case=False, regex=False, na=False))]
    # drop radio edit
    df_tracks = df_tracks.loc[~(df_tracks['track'].str.contains('Radio Edit', case=False, regex=False, na=False))]
    # drop same track in different album
    df_tracks = df_tracks.drop_duplicates(subset=['track'], keep='last')
    df_tracks['release date'] = pd.to_datetime(df_tracks['release date'], infer_datetime_format=True)
    # Normalize BPM
    df_tracks['release date_year'] = df_tracks['release date'].dt.year
    
    return df_tracks


def groupby_df(df):
    df_group = df.groupby(['release date_year']).agg({**{col: ['mean'] for col in ['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM', 'popularity']}, **{'track': ['size']}})
    df_group.columns = ['_'.join(multi_index) for multi_index in df_group.columns.ravel()]
    df_group = df_group.reset_index()
    df_group = df_group.rename(columns={'release date_year': 'release date', 'BPM_mean':'BPM','acousticness_mean': 'acousticness', 'danceability_mean': 'danceability', 'energy_mean': 'energy', 'speechiness_mean': 'speechiness', 'valence_mean': 'valence','popularity_mean':'popularity','track_size':'Number of Tracks'})
    return df_group
