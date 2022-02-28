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
    username = display_user_name()
    pic_url = display_user_pic()
    user_pic = Image.open('../data/interim/user_pic.jpg')
    st.sidebar.text("Welcome %s !" % (username))
    st.sidebar.image(user_pic, width=100)