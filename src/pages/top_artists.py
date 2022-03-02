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
    st.text('Your Top Artists')
    df_top_artists = get_top_artists()
    df_top_artists = df_top_artists.head(5)
    track_urls = list(df_top_artists['url'])
    
    col1, col2 = st.columns(2)
    with col1:
        for artist in df_top_artists['name'].unique():
            df = df_top_artists[df_top_artists['name'] == artist]
            uri = list(df['url'])[0]
            track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="460" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
            components.html(track,height=380, )
            followers = list(df['followers'])[0]
            popularity = list(df['popularity'])[0]
            with st.expander("See more details"):
                st.metric("Followers", followers)
                st.metric("Popularity", popularity)
    