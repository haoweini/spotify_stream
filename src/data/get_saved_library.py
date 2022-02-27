import configparser
import json
import spotipy
import spotipy.util as util
import pandas as pd
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import bamboolib

import warnings
warnings.filterwarnings("ignore")

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = spotify_creds['username']
scope = spotify_creds['scope']
redirect_uri = spotify_creds['redirect_url']

def connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri):
    
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
        
    return sp

sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)

def get_saved_library(sp):
    
    df_saved_tracks = pd.DataFrame()
    track_list = ''
    added_ts_list = []
    artist_list = []
    title_list = []
    popularity_list = []
    album_cover_list = []
    more_songs = True
    offset_index = 0

    while more_songs:
        songs = sp.current_user_saved_tracks(offset=offset_index)
        for song in songs['items']:
            #join track ids to a string for audio_features function
            track_list += song['track']['id'] +','
            #get the time when the song was added
            added_ts_list.append(song['added_at'])
            #get the title of the song
            title_list.append(song['track']['name'])
            #get popularity
            popularity_list.append(song['track']['popularity'])
            album_cover_list.append(song['track']['album']['images'][0]['url'])
            #get all the artists in the song
            artists = song['track']['artists']
            artists_name = ''
            for artist in artists:
                artists_name += artist['name']  + ','
            artist_list.append(artists_name[:-1])
        track_list = ''
        if songs['next'] == None:
            # no more songs in playlist
            more_songs = False
        else:
            # get the next n songs
            offset_index += songs['limit']
    #include timestamp added, title and artists of a song
    df_saved_tracks['song_title'] = title_list
    df_saved_tracks['artists'] = artist_list
    df_saved_tracks['date_added'] = added_ts_list
    df_saved_tracks['album_cover'] = album_cover_list
    df_saved_tracks['popularity'] = popularity_list
    
    return df_saved_tracks