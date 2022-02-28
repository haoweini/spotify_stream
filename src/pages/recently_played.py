import streamlit as st
import numpy as np
import pandas as pd
from dis import dis
import streamlit as st
from data.get_saved_library import get_saved_library, display_user_name, display_user_pic
from data.get_recently_played import get_recently_played
from data.get_top_artists import get_top_artists
from data.image_url import path_to_image_html
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML
import streamlit.components.v1 as components

# @st.cache
def app():
    st.text('You just listened these 6 songs')
    df_recent = get_recently_played()
    df_recent = df_recent.head(6)

    track_urls = list(df_recent['url'])
    tracks = []

    for uri in track_urls:
        track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
        tracks.append(track)

    for track in tracks:
        components.html(track,height=100, )