import os
import streamlit as st
import numpy as np
from PIL import  Image
# Custom imports 
from multipage import MultiPage
#from pages import data_upload, machine_learning, metadata, data_visualize, redundant # import your pages here
from pages import saved_library, artists_main, recently_played, welcome

# Create an instance of the app 
app = MultiPage()

# Title of the main page
#display = Image.open('Logo.png')
#display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
#col1, col2 = st.beta_columns(2)
#col1.image(display, width = 400)

# Set default to wide 
st.set_page_config(layout="wide")
# Title at the top of the application 
st.title("Spotify Streaming")



# Add all your application here
app.add_page("Main Page", welcome.app)
app.add_page("Explore Your Streaming History", saved_library.app)
app.add_page("Find Your Top Artists", artists_main.app)
app.add_page("Recently Played", recently_played.app)

# The main app
app.run()

# Display Developer
me = Image.open('../data/raw/me.jpg')
st.sidebar.image(me,width=100)
st.sidebar.markdown("  \n  \nDeveloped by [Haowei Ni](https://www.linkedin.com/in/haowei-ni-5b9000114/)")
