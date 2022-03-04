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
from data.album_tracks import search_artist_album, find_album_tracks, find_all_tracks_features, groupby_df
from PIL import Image
import requests
import streamlit.components.v1 as components
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# @st.cache
def app():
    artist = st.text_input('Choose An Artist', 'KSHMR')
    with st.container():
        col1, col2, col3 = st.columns([1,0.5,1])
        with col1:
            df_artist = search_random_artist(artist)
            uri = list(df_artist['url'])[0]
            track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="490" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
            components.html(track,height=380, width=500)

            with st.expander("Explore More Artists Similar To Your Pick"):
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
                st.plotly_chart(fig, width=500, use_container_width=True)
    
    with st.container():
        
        df_album = search_artist_album(artist)
        df_all_track_features = find_all_tracks_features(df_album,artist)
        df_all_track_features[['BPM']] = NormalizeData(df_all_track_features[['BPM']])
        df_all_track_features = groupby_df(df_all_track_features)

        trace1 = go.Bar(
        x=df_all_track_features['release date'],
        y=df_all_track_features['Number of Tracks'],
        name = 'Released Tracks',
        )

        trace2 = go.Scatter(
        x = df_all_track_features['release date'],
        y = df_all_track_features['popularity'],
        yaxis='y2',
        line_color='#FF1493',
        name = 'Popularity'
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(trace1)
        fig.add_trace(trace2,secondary_y=True)
        fig['layout'].update(height = 600, width = 1200,xaxis=dict(
        ))
        fig.update_layout(height=500, width=1300)
        st.plotly_chart(fig, width=1300, use_container_width=True)

        options = st.multiselect(
        'Choose Metrics To Explore',
        ['energy', 'speechiness', 'danceability', 'acousticness', 'BPM', 'valence'],
        ['energy'])

        fig = px.line(df_all_track_features.sort_values(by=['release date'], ascending=[True]), x='release date', y=options)
        fig.update_layout(height=500, width=1300)
        st.plotly_chart(fig, width=1300, use_container_width=True)