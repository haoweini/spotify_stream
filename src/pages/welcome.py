import streamlit as st
from dis import dis
import streamlit as st
from data.get_saved_library import display_user_name, get_all_genre, get_saved_library
from data.get_top_artists import get_top_tracks
from PIL import Image
import streamlit.components.v1 as components
import plotly.express as px
import hydralit_components as hc
import time 

# @st.cache
def app():
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            username = display_user_name()
            #pic_url = display_user_pic()
            user_pic = Image.open('../data/raw/user_pic.jpg')
            st.text("Welcome %s !" % (username))
            st.image(user_pic, width=500, use_column_width='always')
        
        with col2:
            st.text('These Are Your Top 5 Tracks')
            df_top_tracks = get_top_tracks()
            df_top_tracks = df_top_tracks.head(5)
            track_urls = list(df_top_tracks['url'])

            for uri in track_urls:
                track = """<iframe src="https://open.spotify.com/embed/track/{}" width="460" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
                components.html(track,height=100, )

    with st.container():
        df_saved = get_saved_library()
        # get all artists in saved library
        with hc.HyLoader("Now Loading Your Top Genres",hc.Loaders.pacman,):
            
            df_artist_detailed_genre = get_all_genre(df_saved)

            genre_new = []
            for i in range(len(df_artist_detailed_genre)):
                genre = df_artist_detailed_genre.iloc[i]['genre']
                if 'pop' in genre:
                    genre_new.append('pop')
                elif 'edm' in genre:
                    genre_new.append('edm')
                elif 'house' in genre:
                    genre_new.append('house')
                elif 'big room' in genre:
                    genre_new.append('big room')
                elif 'trance' in genre:
                    genre_new.append('trance')
                elif 'elect' in genre:
                    genre_new.append('edm')
                elif 'rap' in genre:
                    genre_new.append('rap')
                elif 'dance' in genre:
                    genre_new.append('dance')
                else:
                    genre_new.append('other')
                    
            df_artist_detailed_genre['genre_new'] = genre_new
            fig = px.treemap(df_artist_detailed_genre, path=['genre_new'])
            st.plotly_chart(fig, width=1500, use_container_width=True)