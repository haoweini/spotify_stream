import streamlit as st
import numpy as np
import pandas as pd
from dis import dis
import streamlit as st
from data.get_saved_library import display_user_name, display_user_pic
from data.get_top_artists import get_top_tracks
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML
import streamlit.components.v1 as components

# @st.cache
def app():
    col1, col2 = st.columns(2)
    with col1:
        username = display_user_name()
        #pic_url = display_user_pic()
        user_pic = Image.open('../data/raw/user_pic.jpg')
        st.text("Welcome %s !" % (username))
        st.image(user_pic, width=500, use_container_width='always')
    
    with col2:
        st.text('These Are Your Top 5 Tracks')
        df_top_tracks = get_top_tracks()
        df_top_tracks = df_top_tracks.head(5)
        track_urls = list(df_top_tracks['url'])

        for uri in track_urls:
            track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
            components.html(track,height=100, )