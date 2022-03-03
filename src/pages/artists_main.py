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
from subpage import SubPage
from pages import welcome, artists_top_saved

# @st.cache
def app():

    app_sub = SubPage()
    app_sub.add_page("Main Page", welcome.app)
    app_sub.add_page("Top Artists", artists_top_saved.app)
    app_sub.run()

    #track_urls = list(df_top_artists['url'])
    

    