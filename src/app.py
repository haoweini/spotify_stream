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

# Set default to wide 
st.set_page_config(layout="wide")
# Title at the top of the application 
st.title('Spotify Stream')

col1, col2 = st.columns(2)

# Get Songs from Recently Played
with col1:
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

    # Get Songs from Saved Library
    df_saved = get_saved_library()
    # Select A Song 
    song_title = st.text_input('Select A Song or An Artist From Your Library', 'High On Life')
    df_song = df_saved.loc[(df_saved['song_title'].str.contains(song_title, case=False, regex=False, na=False)) | (df_saved['artists'].str.contains(song_title, case=False, regex=False, na=False))]
    track_urls = list(df_song['url'])
    tracks = []

    for uri in track_urls:
        track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
        tracks.append(track)

    for track in tracks:
        components.html(track,height=100, )

with col2:
    st.text('Your Top Artists')
    df_top_artists = get_top_artists()
    df_top_artists = df_top_artists.head(5)
    track_urls = list(df_top_artists['url'])
    tracks = []
    for uri in track_urls:
        track = """<iframe src="https://open.spotify.com/embed/artist/{}" width="460" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
        components.html(track,height=80, )


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