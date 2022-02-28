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
from data.get_saved_library import  connect_to_spotify_api, display_user_name, display_user_pic
from PIL import Image 

import warnings
warnings.filterwarnings("ignore")

with open('../data/raw/spotify_creds.json') as f:
    spotify_creds = json.load(f)

username = st.text_input('Enter Your User Name', '6oup6y9z3si0zmr49hq1kze9')

client_id = spotify_creds['client_id']
client_secret = spotify_creds['client_secret']
username = username
scope = spotify_creds['recently_played_scope']
redirect_uri = spotify_creds['recently_played_redirect_url']


sp = connect_to_spotify_api(client_id, client_secret, username, scope, redirect_uri)

def display_user_pic():
    user = sp.current_user()
    pic_url = user['images'][0]['url']
    with open('../data/interim/user_pic.jpg', 'wb') as f:
        f.write(requests.get(pic_url).content)
    return pic_url

username = display_user_name()
pic_url = display_user_pic()
user_pic = Image.open('../data/interim/user_pic.jpg')
st.image(user_pic, width=100)