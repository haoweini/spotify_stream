from turtle import width
import streamlit as st
import numpy as np
import pandas as pd
from dis import dis
import streamlit as st
from data.get_saved_library import get_saved_library, display_user_name, display_user_pic
from data.get_recently_played import get_recently_played
from data.get_top_artists import get_top_artists, get_related_artists, get_top_artists_tracks_features, NormalizeData, draw_feature_plot
from data.image_url import path_to_image_html
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML
import streamlit.components.v1 as components
import plotly.express as px
from pages import welcome

# @st.cache
def app():

    #track_urls = list(df_top_artists['url'])
    df_top_artists = get_top_artists()
    df_top_artists = df_top_artists.head(5)

    for artist in df_top_artists['name'].unique():
        col1, col2, col3 = st.columns([1,0.5,1])
        with col1:
            df = df_top_artists[df_top_artists['name'] == artist]
            uri = list(df['url'])[0]
            track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="490" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
            components.html(track,height=400, width=500)
            followers = list(df['followers'])[0]
            followers = (f"{followers:,}")
            popularity = list(df['popularity'])[0]
            with st.expander("Explore More Artists "):
                df_related_artists = get_related_artists(artist)
                df_related_artists = df_related_artists.head(5)
                for related_artist in df_related_artists['name'].unique():
                    df = df_related_artists[df_related_artists['name'] == related_artist]
                    uri = list(df['url'])[0]
                    track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="380" height="100" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
                    components.html(track,height=100, )   

        with col2:
            st.metric("Followers", followers)
            st.metric("Popularity", popularity)
        with col3:
            df_top_track_features = get_top_artists_tracks_features(artist)
            fig = draw_feature_plot(df_top_track_features)
            st.plotly_chart(fig, width=500, use_container_width=True)
    