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

# Title at the top of the application 
st.title('Spotify Stream')

# Get Songs from Recently Played
st.text('You just listened these 5 songs')
df_recent = get_recently_played()
df_recent = df_recent.head(5)
df_recent.to_html('../data/interim/recently_webpage.html',escape=False, formatters=dict(album_cover=path_to_image_html))
HtmlFile = open("../data/interim/recently_webpage.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height =400, width = 1000)

# Get Artists from Top Artists
st.text('Your Top 5 Artists')
df_top_artists = get_top_artists()
df_top_artists = df_top_artists.head(5)
df_top_artists.to_html('../data/interim/top_artists_webpage.html',escape=False, formatters=dict(artist=path_to_image_html))
HtmlFile = open("../data/interim/top_artists_webpage.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height =400, width = 1000)


# Get Songs from Saved Library
df_saved = get_saved_library()

# Select A Song 
song_title = st.text_input('Select A Song or An Artist From Your Library', 'High On Life')
df_song = df_saved.loc[(df_saved['song_title'].str.contains(song_title, case=False, regex=False, na=False)) | (df_saved['artists'].str.contains(song_title, case=False, regex=False, na=False))]
df_song.to_html('../data/interim/webpage.html',escape=False, formatters=dict(album_cover=path_to_image_html))
HtmlFile = open("../data/interim/webpage.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height =3000, width = 1000)


# Side Bar
# Display User
username = display_user_name()
pic_url = display_user_pic()
user_pic = Image.open('../data/interim/user_pic.jpg')
st.sidebar.text("Welcome %s !" % (username))
st.sidebar.image(user_pic, width=100)


# Display Developer
me = Image.open('../data/raw/me.jpg')
st.sidebar.image(me,width=100)
st.sidebar.markdown("  \n  \nDeveloped by [Haowei Ni](https://www.linkedin.com/in/haowei-ni-5b9000114/)")