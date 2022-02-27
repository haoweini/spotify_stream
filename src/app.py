import streamlit as st
from data.get_saved_library import get_saved_library
from PIL import Image
import requests
from io import BytesIO
from IPython.core.display import HTML

# Title at the top of the application 
st.title('Spotify Stream')

df = get_saved_library()

# Select A Song
song_title = st.text_input('Select A Song', 'High On Life')
df_song = df.loc[df['song_title'].str.contains(song_title, case=False, regex=False, na=False)]
df_song_2 = df_song[['song_title','artists','date_added','popularity']]

st.table(df_song_2)
url = list(df_song['album_cover'])[0]
response = requests.get(url)
img = Image.open(BytesIO(response.content))
df_song['image'] = img
st.table(df_song)
st.image(img)
# Select An Artist
#artist_name = st.text_input('Select An Artist', 'Martin Garrix')
#df_artist = df.loc[df['artists'].str.contains(artist_name, case=False, regex=False, na=False)]
#st.table(df_artist)

# Side Bar
me = Image.open('../data/raw/me.jpg')
st.sidebar.image(me,width=100)

st.sidebar.markdown("  \n  \nDeveloped by [Haowei Ni](https://www.linkedin.com/in/haowei-ni-5b9000114/)")