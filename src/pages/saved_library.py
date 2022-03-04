import streamlit as st
import numpy as np
import pandas as pd
from dis import dis
import streamlit as st
from data.get_saved_library import get_saved_library, display_user_name, display_user_pic
from data.get_recently_played import get_recently_played
from data.get_top_artists import get_top_artists, NormalizeData
from data.image_url import path_to_image_html
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML
import streamlit.components.v1 as components
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def groupby_df(df):
    df_group = df.groupby(['date_added_year']).agg({**{col: ['mean'] for col in ['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM', 'popularity']}, **{'track': ['size']}})
    df_group.columns = ['_'.join(multi_index) for multi_index in df_group.columns.ravel()]
    df_group = df_group.reset_index()
    df_group = df_group.rename(columns={'date_added_year': 'date_added_', 'BPM_mean':'BPM','acousticness_mean': 'acousticness', 'danceability_mean': 'danceability', 'energy_mean': 'energy', 'speechiness_mean': 'speechiness', 'valence_mean': 'valence','popularity_mean':'popularity','track_size':'Number of Tracks'})
    return df_group

def groupby_df(df):
    df_group = df.groupby(['date_added_year']).agg({**{col: ['mean'] for col in ['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM', 'popularity']}, **{'song_title': ['size']}})
    df_group.columns = ['_'.join(multi_index) for multi_index in df_group.columns.ravel()]
    df_group = df_group.reset_index()
    df_group = df_group.rename(columns={'date_added_year': 'date_added', 'BPM_mean':'BPM','acousticness_mean': 'acousticness', 'danceability_mean': 'danceability', 'energy_mean': 'energy', 'speechiness_mean': 'speechiness', 'valence_mean': 'valence','popularity_mean':'popularity','song_title_size':'Number of Tracks'})
    return df_group

def draw_feature_plot(df):
    
    df[['BPM']] = NormalizeData(df[['BPM']])

    #df = df.groupby(['artist'])['track', 'acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM'].mean().reset_index()
    df = df[['acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM']]

    fig = px.line_polar(df, r=df.values.flatten(), theta=df.columns, range_r = [0,1.0], line_close=True)
    fig.update_layout(height=500, width=500)
    fig.update_traces(fill='toself')
    
    return fig

# @st.cache
def app():
    st.text('This Is Your Saved Library')
    df_saved = get_saved_library()
    df_saved[['BPM']] = NormalizeData(df_saved[['BPM']])
    # Select A Song 
    song_title = st.text_input('Select A Song or An Artist From Your Library', 'High On Life')
    df_song = df_saved.loc[(df_saved['song_title'].str.contains(song_title, case=False, regex=False, na=False)) | (df_saved['artists'].str.contains(song_title, case=False, regex=False, na=False))]
    with st.expander("Explore More ... "):
        if len(df_song) > 1:
            for song in df_song['song_title']:
                col1, col2= st.columns(2)
                df = df_song[df_song['song_title'] == song]
                track_urls = list(df['url'])[0]
                track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(track_urls)
                with col1:
                    components.html(track,height=400, )
                with col2:
                    fig = draw_feature_plot(df)
                    st.plotly_chart(fig, width=250, use_container_width=True)
        else:
            col1, col2= st.columns(2)
            track_urls = list(df_song['url'])[0]
            track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(track_urls)
            with col1:
                components.html(track,height=400, )
            with col2:
                fig = draw_feature_plot(df_song)
                st.plotly_chart(fig, width=250, use_container_width=True)



    #df_group = groupby_df(df_saved)
    with st.container():
        with st.expander("Sort Tracks By Featuers"):
            metric = st.selectbox(
            "Choose A Metirc You Want To Look At",
            ('acousticness', 'danceability', 'energy', 'speechiness', 'valence', 'BPM', 'popularity','date_added'))
            order = st.radio(
            "In Which Order",
            ('Ascending', 'Decending'))
            if order == 'Ascending':
                order = False
            else:
                order = True

            df_sorted = df_saved.sort_values(by=metric, ascending=order)
            df_sorted = df_sorted.head(5)


            for song in df_sorted['song_title']:
                col1, col2= st.columns(2)
                df = df_sorted[df_sorted['song_title'] == song]
                track_urls = list(df['url'])[0]
                track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(track_urls)
                with col1:
                    components.html(track,height=400, )
                with col2:
                    fig = draw_feature_plot(df)
                    st.plotly_chart(fig, width=250, use_container_width=True)
    
    with st.container():
        with st.expander("Your Streaming History"): 
            #df_saved[['BPM']] = NormalizeData(df_saved[['BPM']])
            df_group = groupby_df(df_saved)
            trace1 = go.Bar(
            x=df_group['date_added'],
            y=df_group['Number of Tracks'],
            name = 'Added Tracks',
            )

            trace2 = go.Scatter(
            x = df_group['date_added'],
            y = df_group['popularity'],
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

            fig = px.line(df_group.sort_values(by=['date_added'], ascending=[True]), x='date_added', y=options)
            fig.update_layout(height=500, width=1300)
            st.plotly_chart(fig, width=1300, use_container_width=True)


    