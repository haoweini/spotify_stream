from turtle import width
import streamlit as st
import numpy as np
import pandas as pd
from dis import dis
import streamlit as st
from data.get_saved_library import get_saved_library, display_user_name, display_user_pic
from data.get_recently_played import get_recently_played
from data.get_top_artists import get_top_artists, get_related_artists, get_top_artists_tracks_features, NormalizeData, draw_feature_plot, search_random_artist
from data.image_url import path_to_image_html
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML
import streamlit.components.v1 as components
import plotly.express as px

# @st.cache
def app():
    artist = st.text_input('Choose An Artist', 'KSHMR')

    col1, col2, col3 = st.columns([1,0.5,1])
    with col1:
        df_artist = search_random_artist(artist)
        uri = list(df_artist['url'])[0]
        track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="490" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
        components.html(track,height=380, width=500)

        with st.expander("Explore More Artists "):
            df_related_artists = get_related_artists(artist)
            df_related_artists = df_related_artists.head(5)
            for related_artist in df_related_artists['name'].unique():
                    df = df_related_artists[df_related_artists['name'] == related_artist]
                    uri = list(df['url'])[0]
                    track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="380" height="100" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
                    components.html(track,height=100, )
    with col2:
        followers = list(df_artist['followers'])[0]
        followers = (f"{followers:,}")
        popularity = list(df_artist['popularity'])[0]
        st.metric("Followers", followers)
        st.metric("Popularity", popularity)

    with col3:
            df_top_track_features = get_top_artists_tracks_features(artist)
            fig = draw_feature_plot(df_top_track_features)
            st.plotly_chart(fig, width=500)